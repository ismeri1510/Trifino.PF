import cx_Oracle

from django.contrib import messages
from django.db import DatabaseError, IntegrityError, connection
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import AutobusForm, FinalizarViajeForm, PilotoForm, RegistrarEncomiendaForm, RutaForm, VenderBoletoForm, ViajeForm
from .models import (
    Autobus,
    Boleto,
    Encomienda,
    LogisticaEncomienda,
    OcupacionRuta,
    Piloto,
    ReporteViaje,
    Ruta,
    Usuario,
    Viaje,
)


def login_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("usuario_id"):
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.session.get("usuario_id"):
        return redirect("dashboard")

    if request.method == "POST":
        correo = request.POST.get("correo", "").strip()
        password = request.POST.get("password", "").strip()

        usuario = Usuario.objects.filter(
            correo__iexact=correo,
            password=password,
            estado__iexact="ACTIVO",
        ).first()

        if usuario:
            request.session["usuario_id"] = usuario.id_usuario
            request.session["usuario_nombre"] = usuario.nombre
            request.session["usuario_rol"] = usuario.rol or ""
            return redirect("dashboard")

        messages.error(request, "Correo o password incorrecto.")

    return render(request, "core/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


@login_requerido
def dashboard_view(request):
    total_buses = Autobus.objects.count()
    viajes_activos = Viaje.objects.filter(estado__iexact="PROGRAMADO").count()
    boletos_vendidos = Boleto.objects.exclude(estado__iexact="ANULADO").count()
    encomiendas_pendientes = Encomienda.objects.filter(
        Q(estado__iexact="PENDIENTE") | Q(estado__iexact="EN TRANSITO")
    ).count()
    ingresos = ReporteViaje.objects.aggregate(total=Sum("ingresos_totales"))
    ruta_mayor_ocupacion = OcupacionRuta.objects.order_by("-porcentaje_ocupacion").first()
    ultimos_viajes = ReporteViaje.objects.order_by("-fecha_salida")[:5]
    ultimas_encomiendas = LogisticaEncomienda.objects.order_by("-fecha_envio")[:5]

    contexto = {
        "total_buses": total_buses,
        "viajes_activos": viajes_activos,
        "boletos_vendidos": boletos_vendidos,
        "encomiendas_pendientes": encomiendas_pendientes,
        "ingresos_totales": ingresos["total"] or 0,
        "ruta_mayor_ocupacion": ruta_mayor_ocupacion,
        "ultimos_viajes": ultimos_viajes,
        "ultimas_encomiendas": ultimas_encomiendas,
    }
    return render(request, "core/dashboard.html", contexto)


@login_requerido
def autobuses_list(request):
    buses = Autobus.objects.all().order_by("id_autobus")
    return render(request, "core/autobuses/list.html", {"buses": buses})


@login_requerido
@require_http_methods(["GET", "POST"])
def autobuses_crear(request):
    form = AutobusForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Autobus registrado correctamente.")
            return redirect("autobuses_list")
        except IntegrityError:
            messages.error(request, "No se pudo guardar. Verifica que la placa no este repetida.")
        except DatabaseError as error:
            messages.error(request, f"Error de base de datos: {error}")

    return render(request, "core/autobuses/form.html", {"form": form, "titulo": "Nuevo autobus"})


@login_requerido
@require_http_methods(["GET", "POST"])
def autobuses_editar(request, id_autobus):
    autobus = get_object_or_404(Autobus, id_autobus=id_autobus)
    form = AutobusForm(request.POST or None, instance=autobus)

    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Autobus actualizado correctamente.")
            return redirect("autobuses_list")
        except IntegrityError:
            messages.error(request, "No se pudo actualizar. Verifica que la placa no este repetida.")
        except DatabaseError as error:
            messages.error(request, f"Error de base de datos: {error}")

    return render(request, "core/autobuses/form.html", {"form": form, "titulo": "Editar autobus"})


@login_requerido
@require_http_methods(["GET", "POST"])
def autobuses_eliminar(request, id_autobus):
    autobus = get_object_or_404(Autobus, id_autobus=id_autobus)

    if request.method == "POST":
        try:
            autobus.delete()
            messages.success(request, "Autobus eliminado correctamente.")
            return redirect("autobuses_list")
        except DatabaseError:
            messages.error(
                request,
                "No se puede eliminar este autobus porque tiene viajes o mantenimientos relacionados.",
            )
            return redirect("autobuses_list")

    return render(request, "core/autobuses/confirm_delete.html", {"autobus": autobus})


def obtener_mensaje_oracle(error):
    texto = str(error)
    if "ORA-" in texto:
        return texto
    return "La base de datos rechazo la operacion."


@login_requerido
def rutas_list(request):
    rutas = Ruta.objects.all().order_by("id_ruta")
    return render(request, "core/rutas/list.html", {"rutas": rutas})


@login_requerido
@require_http_methods(["GET", "POST"])
def rutas_crear(request):
    form = RutaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Ruta registrada correctamente.")
            return redirect("rutas_list")
        except DatabaseError as error:
            messages.error(request, obtener_mensaje_oracle(error))
    return render(request, "core/rutas/form.html", {"form": form, "titulo": "Nueva ruta"})


@login_requerido
@require_http_methods(["GET", "POST"])
def rutas_editar(request, id_ruta):
    ruta = get_object_or_404(Ruta, id_ruta=id_ruta)
    form = RutaForm(request.POST or None, instance=ruta)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Ruta actualizada correctamente.")
            return redirect("rutas_list")
        except DatabaseError as error:
            messages.error(request, obtener_mensaje_oracle(error))
    return render(request, "core/rutas/form.html", {"form": form, "titulo": "Editar ruta"})


@login_requerido
@require_http_methods(["GET", "POST"])
def rutas_eliminar(request, id_ruta):
    ruta = get_object_or_404(Ruta, id_ruta=id_ruta)
    if request.method == "POST":
        try:
            ruta.delete()
            messages.success(request, "Ruta eliminada correctamente.")
            return redirect("rutas_list")
        except DatabaseError:
            messages.error(request, "No se puede eliminar esta ruta porque tiene viajes relacionados.")
            return redirect("rutas_list")
    return render(request, "core/rutas/confirm_delete.html", {"ruta": ruta})


@login_requerido
def pilotos_list(request):
    pilotos = Piloto.objects.all().order_by("id_piloto")
    return render(request, "core/pilotos/list.html", {"pilotos": pilotos})


@login_requerido
@require_http_methods(["GET", "POST"])
def pilotos_crear(request):
    form = PilotoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Piloto registrado correctamente.")
            return redirect("pilotos_list")
        except IntegrityError:
            messages.error(request, "No se pudo guardar. Verifica que el DPI no este repetido.")
        except DatabaseError as error:
            messages.error(request, obtener_mensaje_oracle(error))
    return render(request, "core/pilotos/form.html", {"form": form, "titulo": "Nuevo piloto"})


@login_requerido
@require_http_methods(["GET", "POST"])
def pilotos_editar(request, id_piloto):
    piloto = get_object_or_404(Piloto, id_piloto=id_piloto)
    form = PilotoForm(request.POST or None, instance=piloto)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Piloto actualizado correctamente.")
            return redirect("pilotos_list")
        except IntegrityError:
            messages.error(request, "No se pudo actualizar. Verifica que el DPI no este repetido.")
        except DatabaseError as error:
            messages.error(request, obtener_mensaje_oracle(error))
    return render(request, "core/pilotos/form.html", {"form": form, "titulo": "Editar piloto"})


@login_requerido
@require_http_methods(["GET", "POST"])
def pilotos_eliminar(request, id_piloto):
    piloto = get_object_or_404(Piloto, id_piloto=id_piloto)
    if request.method == "POST":
        try:
            piloto.delete()
            messages.success(request, "Piloto eliminado correctamente.")
            return redirect("pilotos_list")
        except DatabaseError:
            messages.error(request, "No se puede eliminar este piloto porque tiene viajes relacionados.")
            return redirect("pilotos_list")
    return render(request, "core/pilotos/confirm_delete.html", {"piloto": piloto})


@login_requerido
def viajes_list(request):
    viajes = Viaje.objects.select_related("ruta", "autobus", "piloto").all().order_by("id_viaje")
    return render(request, "core/viajes/list.html", {"viajes": viajes})


@login_requerido
@require_http_methods(["GET", "POST"])
def viajes_crear(request):
    form = ViajeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Viaje programado correctamente.")
            return redirect("viajes_list")
        except DatabaseError as error:
            messages.error(request, obtener_mensaje_oracle(error))
    return render(request, "core/viajes/form.html", {"form": form, "titulo": "Nuevo viaje"})


@login_requerido
@require_http_methods(["GET", "POST"])
def viajes_editar(request, id_viaje):
    viaje = get_object_or_404(Viaje, id_viaje=id_viaje)
    form = ViajeForm(request.POST or None, instance=viaje)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
            messages.success(request, "Viaje actualizado correctamente.")
            return redirect("viajes_list")
        except DatabaseError as error:
            messages.error(request, obtener_mensaje_oracle(error))
    return render(request, "core/viajes/form.html", {"form": form, "titulo": "Editar viaje"})


@login_requerido
@require_http_methods(["GET", "POST"])
def viajes_eliminar(request, id_viaje):
    viaje = get_object_or_404(Viaje, id_viaje=id_viaje)
    if request.method == "POST":
        try:
            viaje.delete()
            messages.success(request, "Viaje eliminado correctamente.")
            return redirect("viajes_list")
        except DatabaseError:
            messages.error(request, "No se puede eliminar este viaje porque tiene boletos o encomiendas relacionadas.")
            return redirect("viajes_list")
    return render(request, "core/viajes/confirm_delete.html", {"viaje": viaje})


@login_requerido
@require_http_methods(["GET", "POST"])
def viajes_finalizar(request, id_viaje):
    viaje = get_object_or_404(Viaje.objects.select_related("ruta", "autobus", "piloto"), id_viaje=id_viaje)
    form = FinalizarViajeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        fecha_fin = form.cleaned_data["fecha_fin"]
        usuario_sistema = request.session.get("usuario_rol") or request.session.get("usuario_nombre") or "DJANGO"

        try:
            with connection.cursor() as cursor:
                raw_cursor = cursor.cursor.cursor
                raw_cursor.callproc(
                    "sp_finalizar_viaje",
                    [
                        viaje.id_viaje,
                        fecha_fin,
                        usuario_sistema,
                    ],
                )

            messages.success(request, "Viaje finalizado correctamente.")
            return redirect("viajes_list")
        except (DatabaseError, cx_Oracle.Error) as error:
            messages.error(request, obtener_mensaje_oracle(error))

    return render(request, "core/viajes/finalizar.html", {"form": form, "viaje": viaje})


@login_requerido
@require_http_methods(["GET", "POST"])
def boletos_vender(request):
    form = VenderBoletoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        pasajero = form.cleaned_data["pasajero"]
        viaje = form.cleaned_data["viaje"]
        numero_asiento = form.cleaned_data["numero_asiento"]
        usuario_sistema = request.session.get("usuario_rol") or request.session.get("usuario_nombre") or "DJANGO"

        try:
            with connection.cursor() as cursor:
                raw_cursor = cursor.cursor.cursor
                id_boleto = raw_cursor.var(int)
                raw_cursor.callproc(
                    "sp_vender_boleto",
                    [
                        pasajero.id_pasajero,
                        viaje.id_viaje,
                        numero_asiento,
                        usuario_sistema,
                        id_boleto,
                    ],
                )
                nuevo_id = id_boleto.getvalue()

            messages.success(request, f"Boleto vendido correctamente. ID boleto: {nuevo_id}.")
            return redirect("boletos_vender")
        except (DatabaseError, cx_Oracle.Error) as error:
            messages.error(request, obtener_mensaje_oracle(error))

    return render(request, "core/boletos/vender.html", {"form": form})


@login_requerido
@require_http_methods(["GET", "POST"])
def encomiendas_registrar(request):
    form = RegistrarEncomiendaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        remitente = form.cleaned_data["remitente"]
        destinatario = form.cleaned_data["destinatario"]
        viaje = form.cleaned_data["viaje"]
        peso = form.cleaned_data["peso"]
        descripcion = form.cleaned_data["descripcion"]
        usuario_sistema = request.session.get("usuario_rol") or request.session.get("usuario_nombre") or "DJANGO"

        try:
            with connection.cursor() as cursor:
                raw_cursor = cursor.cursor.cursor
                id_encomienda = raw_cursor.var(int)
                codigo_rastreo = raw_cursor.var(str)
                raw_cursor.callproc(
                    "sp_registrar_encomienda",
                    [
                        remitente.id_cliente,
                        destinatario.id_cliente,
                        viaje.id_viaje,
                        peso,
                        descripcion,
                        usuario_sistema,
                        id_encomienda,
                        codigo_rastreo,
                    ],
                )

            messages.success(
                request,
                f"Encomienda registrada correctamente. Codigo: {codigo_rastreo.getvalue()}.",
            )
            return redirect("encomiendas_registrar")
        except (DatabaseError, cx_Oracle.Error) as error:
            messages.error(request, obtener_mensaje_oracle(error))

    return render(request, "core/encomiendas/registrar.html", {"form": form})


@login_requerido
def reporte_viajes(request):
    viajes = ReporteViaje.objects.all().order_by("-fecha_salida", "id_viaje")
    return render(request, "core/reportes/viajes.html", {"viajes": viajes})


@login_requerido
def reporte_ocupacion_rutas(request):
    rutas = OcupacionRuta.objects.all().order_by("-porcentaje_ocupacion")
    return render(request, "core/reportes/ocupacion_rutas.html", {"rutas": rutas})


@login_requerido
def reporte_encomiendas(request):
    encomiendas = LogisticaEncomienda.objects.all().order_by("-fecha_envio", "id_encomienda")
    return render(request, "core/reportes/encomiendas.html", {"encomiendas": encomiendas})

from django import forms

from .models import Autobus, ClienteEncomienda, Pasajero, Piloto, Ruta, Viaje


class AutobusForm(forms.ModelForm):
    class Meta:
        model = Autobus
        fields = ["placa", "modelo", "capacidad", "estado"]
        labels = {
            "placa": "Placa",
            "modelo": "Modelo",
            "capacidad": "Capacidad",
            "estado": "Estado",
        }
        widgets = {
            "placa": forms.TextInput(attrs={"class": "form-control", "placeholder": "C-123ABC"}),
            "modelo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mercedes Benz 2020"}),
            "capacidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "placeholder": "DISPONIBLE"}),
        }


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ["origen", "destino", "distancia_km", "precio_base", "duracion"]
        labels = {
            "origen": "Origen",
            "destino": "Destino",
            "distancia_km": "Distancia km",
            "precio_base": "Precio base",
            "duracion": "Duracion",
        }
        widgets = {
            "origen": forms.TextInput(attrs={"class": "form-control"}),
            "destino": forms.TextInput(attrs={"class": "form-control"}),
            "distancia_km": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "precio_base": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
            "duracion": forms.TextInput(attrs={"class": "form-control", "placeholder": "4 horas"}),
        }


class PilotoForm(forms.ModelForm):
    class Meta:
        model = Piloto
        fields = ["nombre", "dpi", "telefono", "licencia", "estado"]
        labels = {
            "nombre": "Nombre",
            "dpi": "DPI",
            "telefono": "Telefono",
            "licencia": "Licencia",
            "estado": "Estado",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "dpi": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "licencia": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "placeholder": "ACTIVO"}),
        }


class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ["ruta", "autobus", "piloto", "fecha_salida", "hora_salida", "estado", "fecha_fin"]
        labels = {
            "ruta": "Ruta",
            "autobus": "Autobus",
            "piloto": "Piloto",
            "fecha_salida": "Fecha salida",
            "hora_salida": "Hora salida",
            "estado": "Estado",
            "fecha_fin": "Fecha fin",
        }
        widgets = {
            "ruta": forms.Select(attrs={"class": "form-select"}),
            "autobus": forms.Select(attrs={"class": "form-select"}),
            "piloto": forms.Select(attrs={"class": "form-select"}),
            "fecha_salida": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "hora_salida": forms.TextInput(attrs={"class": "form-control", "placeholder": "08:00 AM"}),
            "estado": forms.TextInput(attrs={"class": "form-control", "placeholder": "PROGRAMADO"}),
            "fecha_fin": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class VenderBoletoForm(forms.Form):
    pasajero = forms.ModelChoiceField(
        queryset=Pasajero.objects.all().order_by("nombre"),
        label="Pasajero",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    viaje = forms.ModelChoiceField(
        queryset=Viaje.objects.filter(estado__iexact="PROGRAMADO").order_by("fecha_salida", "hora_salida"),
        label="Viaje programado",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    numero_asiento = forms.IntegerField(
        label="Numero de asiento",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )


class RegistrarEncomiendaForm(forms.Form):
    remitente = forms.ModelChoiceField(
        queryset=ClienteEncomienda.objects.all().order_by("nombre"),
        label="Remitente",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    destinatario = forms.ModelChoiceField(
        queryset=ClienteEncomienda.objects.all().order_by("nombre"),
        label="Destinatario",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    viaje = forms.ModelChoiceField(
        queryset=Viaje.objects.filter(estado__iexact="PROGRAMADO").order_by("fecha_salida", "hora_salida"),
        label="Viaje programado",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    peso = forms.DecimalField(
        label="Peso",
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "0.01", "step": "0.01"}),
    )
    descripcion = forms.CharField(
        label="Descripcion",
        max_length=200,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )


class FinalizarViajeForm(forms.Form):
    fecha_fin = forms.DateField(
        label="Fecha fin",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

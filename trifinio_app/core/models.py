from django.db import models


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, db_column="ID_USUARIO")
    nombre = models.CharField(max_length=100, db_column="NOMBRE")
    correo = models.CharField(max_length=100, unique=True, db_column="CORREO")
    password = models.CharField(max_length=100, db_column="PASSWORD")
    rol = models.CharField(max_length=30, blank=True, null=True, db_column="ROL")
    estado = models.CharField(max_length=20, blank=True, null=True, db_column="ESTADO")

    class Meta:
        managed = False
        db_table = "USUARIOS"

    def __str__(self):
        return self.nombre


class Autobus(models.Model):
    id_autobus = models.AutoField(primary_key=True, db_column="ID_AUTOBUS")
    placa = models.CharField(max_length=20, unique=True, db_column="PLACA")
    modelo = models.CharField(max_length=50, blank=True, null=True, db_column="MODELO")
    capacidad = models.IntegerField(db_column="CAPACIDAD")
    estado = models.CharField(max_length=30, blank=True, null=True, db_column="ESTADO")

    class Meta:
        managed = False
        db_table = "AUTOBUSES"

    def __str__(self):
        return self.placa


class Piloto(models.Model):
    id_piloto = models.AutoField(primary_key=True, db_column="ID_PILOTO")
    nombre = models.CharField(max_length=100, db_column="NOMBRE")
    dpi = models.CharField(max_length=20, unique=True, blank=True, null=True, db_column="DPI")
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column="TELEFONO")
    licencia = models.CharField(max_length=30, blank=True, null=True, db_column="LICENCIA")
    estado = models.CharField(max_length=20, blank=True, null=True, db_column="ESTADO")

    class Meta:
        managed = False
        db_table = "PILOTOS"

    def __str__(self):
        return self.nombre


class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True, db_column="ID_RUTA")
    origen = models.CharField(max_length=100, blank=True, null=True, db_column="ORIGEN")
    destino = models.CharField(max_length=100, blank=True, null=True, db_column="DESTINO")
    distancia_km = models.IntegerField(blank=True, null=True, db_column="DISTANCIA_KM")
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="PRECIO_BASE")
    duracion = models.CharField(max_length=30, blank=True, null=True, db_column="DURACION")

    class Meta:
        managed = False
        db_table = "RUTAS"

    def __str__(self):
        return f"{self.origen} - {self.destino}"


class Pasajero(models.Model):
    id_pasajero = models.AutoField(primary_key=True, db_column="ID_PASAJERO")
    nombre = models.CharField(max_length=100, blank=True, null=True, db_column="NOMBRE")
    dpi = models.CharField(max_length=20, blank=True, null=True, db_column="DPI")
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column="TELEFONO")
    correo = models.CharField(max_length=100, blank=True, null=True, db_column="CORREO")

    class Meta:
        managed = False
        db_table = "PASAJEROS"

    def __str__(self):
        return self.nombre or f"Pasajero {self.id_pasajero}"


class ClienteEncomienda(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column="ID_CLIENTE")
    nombre = models.CharField(max_length=100, blank=True, null=True, db_column="NOMBRE")
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column="TELEFONO")
    direccion = models.CharField(max_length=200, blank=True, null=True, db_column="DIRECCION")
    dpi = models.CharField(max_length=20, blank=True, null=True, db_column="DPI")

    class Meta:
        managed = False
        db_table = "CLIENTES_ENCOMIENDA"

    def __str__(self):
        return self.nombre or f"Cliente {self.id_cliente}"


class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True, db_column="ID_VIAJE")
    ruta = models.ForeignKey(Ruta, on_delete=models.DO_NOTHING, db_column="ID_RUTA")
    autobus = models.ForeignKey(Autobus, on_delete=models.DO_NOTHING, db_column="ID_AUTOBUS")
    piloto = models.ForeignKey(Piloto, on_delete=models.DO_NOTHING, db_column="ID_PILOTO")
    fecha_salida = models.DateField(blank=True, null=True, db_column="FECHA_SALIDA")
    hora_salida = models.CharField(max_length=10, blank=True, null=True, db_column="HORA_SALIDA")
    estado = models.CharField(max_length=30, blank=True, null=True, db_column="ESTADO")
    fecha_fin = models.DateField(blank=True, null=True, db_column="FECHA_FIN")

    class Meta:
        managed = False
        db_table = "VIAJES"

    def __str__(self):
        return f"Viaje {self.id_viaje}"


class Boleto(models.Model):
    id_boleto = models.AutoField(primary_key=True, db_column="ID_BOLETO")
    pasajero = models.ForeignKey(Pasajero, on_delete=models.DO_NOTHING, db_column="ID_PASAJERO")
    viaje = models.ForeignKey(Viaje, on_delete=models.DO_NOTHING, db_column="ID_VIAJE")
    numero_asiento = models.IntegerField(db_column="NUMERO_ASIENTO")
    fecha_compra = models.DateField(blank=True, null=True, db_column="FECHA_COMPRA")
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="PRECIO")
    estado = models.CharField(max_length=20, blank=True, null=True, db_column="ESTADO")

    class Meta:
        managed = False
        db_table = "BOLETOS"

    def __str__(self):
        return f"Boleto {self.id_boleto}"


class Encomienda(models.Model):
    id_encomienda = models.AutoField(primary_key=True, db_column="ID_ENCOMIENDA")
    remitente = models.ForeignKey(
        ClienteEncomienda,
        on_delete=models.DO_NOTHING,
        db_column="ID_REMITENTE",
        related_name="encomiendas_enviadas",
    )
    destinatario = models.ForeignKey(
        ClienteEncomienda,
        on_delete=models.DO_NOTHING,
        db_column="ID_DESTINATARIO",
        related_name="encomiendas_recibidas",
    )
    viaje = models.ForeignKey(Viaje, on_delete=models.DO_NOTHING, db_column="ID_VIAJE")
    peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="PESO")
    descripcion = models.CharField(max_length=200, blank=True, null=True, db_column="DESCRIPCION")
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="COSTO")
    codigo_rastreo = models.CharField(max_length=50, unique=True, blank=True, null=True, db_column="CODIGO_RASTREO")
    estado = models.CharField(max_length=30, blank=True, null=True, db_column="ESTADO")
    fecha_envio = models.DateField(blank=True, null=True, db_column="FECHA_ENVIO")

    class Meta:
        managed = False
        db_table = "ENCOMIENDAS"

    def __str__(self):
        return self.codigo_rastreo or f"Encomienda {self.id_encomienda}"


class Mantenimiento(models.Model):
    id_mantenimiento = models.AutoField(primary_key=True, db_column="ID_MANTENIMIENTO")
    autobus = models.ForeignKey(Autobus, on_delete=models.DO_NOTHING, db_column="ID_AUTOBUS")
    fecha = models.DateField(blank=True, null=True, db_column="FECHA")
    descripcion = models.CharField(max_length=200, blank=True, null=True, db_column="DESCRIPCION")
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="COSTO")
    tipo = models.CharField(max_length=50, blank=True, null=True, db_column="TIPO")

    class Meta:
        managed = False
        db_table = "MANTENIMIENTOS"

    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento}"


class Auditoria(models.Model):
    id_auditoria = models.AutoField(primary_key=True, db_column="ID_AUDITORIA")
    tabla_afectada = models.CharField(max_length=50, blank=True, null=True, db_column="TABLA_AFECTADA")
    accion = models.CharField(max_length=20, blank=True, null=True, db_column="ACCION")
    usuario_sistema = models.CharField(max_length=100, blank=True, null=True, db_column="USUARIO_SISTEMA")
    fecha_accion = models.DateField(blank=True, null=True, db_column="FECHA_ACCION")
    descripcion = models.CharField(max_length=200, blank=True, null=True, db_column="DESCRIPCION")

    class Meta:
        managed = False
        db_table = "AUDITORIA"

    def __str__(self):
        return f"{self.tabla_afectada} - {self.accion}"


class ReporteViaje(models.Model):
    id_viaje = models.IntegerField(primary_key=True, db_column="ID_VIAJE")
    origen = models.CharField(max_length=100, blank=True, null=True, db_column="ORIGEN")
    destino = models.CharField(max_length=100, blank=True, null=True, db_column="DESTINO")
    fecha_salida = models.DateField(blank=True, null=True, db_column="FECHA_SALIDA")
    hora_salida = models.CharField(max_length=10, blank=True, null=True, db_column="HORA_SALIDA")
    fecha_fin = models.DateField(blank=True, null=True, db_column="FECHA_FIN")
    estado = models.CharField(max_length=30, blank=True, null=True, db_column="ESTADO")
    placa = models.CharField(max_length=20, blank=True, null=True, db_column="PLACA")
    modelo = models.CharField(max_length=50, blank=True, null=True, db_column="MODELO")
    capacidad = models.IntegerField(blank=True, null=True, db_column="CAPACIDAD")
    piloto = models.CharField(max_length=100, blank=True, null=True, db_column="PILOTO")
    boletos_vendidos = models.IntegerField(blank=True, null=True, db_column="BOLETOS_VENDIDOS")
    asientos_disponibles = models.IntegerField(blank=True, null=True, db_column="ASIENTOS_DISPONIBLES")
    ingresos_boletos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="INGRESOS_BOLETOS")
    encomiendas_registradas = models.IntegerField(blank=True, null=True, db_column="ENCOMIENDAS_REGISTRADAS")
    ingresos_encomiendas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="INGRESOS_ENCOMIENDAS")
    ingresos_totales = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="INGRESOS_TOTALES")

    class Meta:
        managed = False
        db_table = "VW_REPORTE_VIAJES"


class OcupacionRuta(models.Model):
    id_ruta = models.IntegerField(primary_key=True, db_column="ID_RUTA")
    origen = models.CharField(max_length=100, blank=True, null=True, db_column="ORIGEN")
    destino = models.CharField(max_length=100, blank=True, null=True, db_column="DESTINO")
    total_viajes = models.IntegerField(blank=True, null=True, db_column="TOTAL_VIAJES")
    capacidad_total = models.IntegerField(blank=True, null=True, db_column="CAPACIDAD_TOTAL")
    boletos_vendidos = models.IntegerField(blank=True, null=True, db_column="BOLETOS_VENDIDOS")
    porcentaje_ocupacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="PORCENTAJE_OCUPACION")
    ingresos_boletos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="INGRESOS_BOLETOS")

    class Meta:
        managed = False
        db_table = "VW_OCUPACION_RUTAS"


class LogisticaEncomienda(models.Model):
    id_encomienda = models.IntegerField(primary_key=True, db_column="ID_ENCOMIENDA")
    codigo_rastreo = models.CharField(max_length=50, blank=True, null=True, db_column="CODIGO_RASTREO")
    remitente = models.CharField(max_length=100, blank=True, null=True, db_column="REMITENTE")
    destinatario = models.CharField(max_length=100, blank=True, null=True, db_column="DESTINATARIO")
    origen = models.CharField(max_length=100, blank=True, null=True, db_column="ORIGEN")
    destino = models.CharField(max_length=100, blank=True, null=True, db_column="DESTINO")
    fecha_salida = models.DateField(blank=True, null=True, db_column="FECHA_SALIDA")
    hora_salida = models.CharField(max_length=10, blank=True, null=True, db_column="HORA_SALIDA")
    peso = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="PESO")
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column="COSTO")
    estado = models.CharField(max_length=30, blank=True, null=True, db_column="ESTADO")
    fecha_envio = models.DateField(blank=True, null=True, db_column="FECHA_ENVIO")

    class Meta:
        managed = False
        db_table = "VW_LOGISTICA_ENCOMIENDAS"

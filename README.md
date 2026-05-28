# Rutas del Trifinio

Proyecto universitario para el curso de Bases de Datos II. La aplicacion integra una base de datos Oracle con Django, priorizando el uso de estructuras avanzadas de base de datos: procedures, views y triggers.

## Enfoque del proyecto

- Arquitectura monolitica con Django.
- Frontend con Django Templates y Bootstrap.
- Backend y vistas HTML dentro del mismo proyecto.
- Conexion a Oracle usando ORM de Django y llamadas directas a procedures.
- Codigo simple y mantenible, acorde a un proyecto academico.

No se utiliza React, Vite, SPA, JWT, microservicios ni frontend desacoplado.

## Estructura

```text
Proyecto final/
├── trifinio_app/
│   ├── core/
│   ├── static/
│   ├── templates/
│   ├── trifinio/
│   ├── .env
│   ├── .venv310/
│   ├── manage.py
│   └── requirements.txt
├── tables.sql
├── seeds.sql
├── views.sql
├── triggers.sql
├── procedures.sql
├── PLAN_DESARROLLO.md
└── README.md
```

## Requisitos

- Python 3.10.
- Oracle 18c.
- Usuario Oracle creado para el proyecto.
- Scripts SQL ejecutados en Oracle:
  - `tables.sql`
  - `seeds.sql`
  - `views.sql`
  - `triggers.sql`
  - `procedures.sql`

## Configuracion

El archivo `.env` debe estar dentro de `trifinio_app/`:

```env
DB_NAME=localhost:1521/XEPDB1
DB_USER=TRIFINIO.PF
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE_NAME=XEPDB1
```

## Instalacion y ejecucion

Entrar a la carpeta de la aplicacion:

```powershell
cd "C:\Users\ismer\Documents\UMG\SEMESTRE VII\Base de Datos II\Proyecto final\trifinio_app"
```

Activar el entorno virtual:

```powershell
.\.venv310\Scripts\Activate.ps1
```

Instalar dependencias si fuera necesario:

```powershell
pip install -r requirements.txt
```

Verificar configuracion:

```powershell
python manage.py check
```

Ejecutar servidor:

```powershell
python manage.py runserver
```

Abrir en el navegador:

```text
http://127.0.0.1:8000/login/
```

## Usuario de prueba

```text
Correo: admin@trifinio.com
Password: admin123
```

## Modulos implementados

### Login y Dashboard

- Login usando la tabla `usuarios`.
- Sesion simple con cookies firmadas.
- Dashboard con resumen de buses, viajes, boletos y encomiendas.
- Resumen gerencial consumiendo vistas de Oracle.

### CRUDs

- Autobuses.
- Rutas.
- Pilotos.
- Viajes.

Estos CRUDs permiten probar las reglas de negocio implementadas con triggers.

### Procedures

Se integran desde Django mediante `connection.cursor()`:

- `sp_vender_boleto`
  - Pantalla: `/boletos/vender/`
  - Valida pasajero, viaje programado, asiento disponible y capacidad.
  - Registra boleto y auditoria.

- `sp_registrar_encomienda`
  - Pantalla: `/encomiendas/registrar/`
  - Valida remitente, destinatario, peso y viaje.
  - Calcula costo, genera codigo de rastreo y registra auditoria.

- `sp_finalizar_viaje`
  - Pantalla: `/viajes/<id>/finalizar/`
  - Finaliza viaje, libera autobus, actualiza encomiendas y registra auditoria.

### Triggers

Los triggers se prueban desde el modulo de viajes:

- `trg_no_modificar_viaje_finalizado`
  - Evita modificar un viaje con estado `FINALIZADO`.

- `trg_validar_autobus_disponible`
  - Evita programar dos viajes con el mismo autobus en la misma fecha y hora.

### Views / Reportes

Las vistas Oracle se consumen en pantallas de solo lectura:

- `/reportes/viajes/`
  - Usa `vw_reporte_viajes`.

- `/reportes/ocupacion-rutas/`
  - Usa `vw_ocupacion_rutas`.

- `/reportes/encomiendas/`
  - Usa `vw_logistica_encomiendas`.

## Pruebas sugeridas

### Trigger de autobus ocupado

Crear un viaje con el mismo autobus, fecha y hora de otro viaje programado. Oracle debe rechazarlo.

### Trigger de viaje finalizado

Editar un viaje con estado `FINALIZADO`. Oracle debe rechazar la modificacion.

### Procedure de venta de boleto

Vender un boleto en un asiento libre. Luego intentar vender el mismo asiento otra vez para ver el error.

### Procedure de encomienda

Registrar una encomienda con remitente y destinatario diferentes. Luego intentar usar el mismo cliente como remitente y destinatario para ver el error.

### Procedure de finalizar viaje

Finalizar un viaje programado con fecha valida. Luego intentar finalizar un viaje que ya esta finalizado para ver el error.

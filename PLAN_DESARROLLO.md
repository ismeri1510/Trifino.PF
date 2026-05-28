# Plan de Desarrollo Django Monolitico - Rutas del Trifinio

## Resumen

Desarrollar una aplicacion universitaria monolitica en Django conectada a Oracle, usando ORM para tablas/vistas existentes, Django Templates para las pantallas HTML y Bootstrap para estilos. El foco sera integrar correctamente la base de datos ya disenada: tablas, procedures, views y triggers, manteniendo el codigo simple, claro y facil de defender.

## Base Actual Revisada

El enunciado exige:

- Modulos minimos: flota/mantenimiento, rutas/viajes, venta de boletos, encomiendas/logistica.
- PL/SQL: 3 vistas, 3 procedures transaccionales y 2 triggers.
- Prototipo funcional: login, CRUD completo, modulo transaccional que invoque un procedure Oracle y dashboard/reporte consumiendo vistas.

Los SQL actuales ya cubren:

- Tablas principales: `usuarios`, `autobuses`, `pilotos`, `rutas`, `pasajeros`, `clientes_encomienda`, `viajes`, `boletos`, `encomiendas`, `mantenimientos`, `auditoria`.
- Procedures: `sp_vender_boleto`, `sp_registrar_encomienda`, `sp_finalizar_viaje`.
- Views: `vw_reporte_viajes`, `vw_ocupacion_rutas`, `vw_logistica_encomiendas`.
- Triggers: bloqueo de modificacion de viajes finalizados y validacion de bus ocupado.

Antes de ejecutar scripts, separar o comentar consultas de prueba y corregir la linea no comentada `==========================================================` en `procedures.sql`.

## Implementacion Django

- Crear proyecto Django monolitico con conexion Oracle mediante driver compatible (`oracledb`/backend Oracle de Django).
- Modelar tablas existentes con ORM usando `managed = False`, para que Django no intente recrear la estructura Oracle.
- Modelar las vistas como modelos de solo lectura, tambien `managed = False`.
- Usar Django Templates para las pantallas HTML y Bootstrap para estilos.
- Usar la tabla `usuarios` existente para login simple por `correo` y `password`, guardando datos basicos del usuario en la sesion.
- Mantener permisos simples: las vistas protegidas validaran que exista un usuario activo en sesion, sin arquitectura compleja de roles.

Vistas y rutas web propuestas:

- `/login/`: formulario de inicio de sesion.
- `/logout/`: cierre de sesion.
- `/`: dashboard principal.
- CRUD:
  - `/autobuses/`
  - `/pilotos/`
  - `/rutas/`
  - `/pasajeros/`
  - `/clientes-encomienda/`
  - `/viajes/`
  - `/mantenimientos/`
- Transaccionales:
  - `/boletos/vender/`: formulario que llama `sp_vender_boleto`
  - `/encomiendas/registrar/`: formulario que llama `sp_registrar_encomienda`
  - `/viajes/<id>/finalizar/`: accion que llama `sp_finalizar_viaje`
- Reportes:
  - `/reportes/viajes/` consume `vw_reporte_viajes`
  - `/reportes/ocupacion-rutas/` consume `vw_ocupacion_rutas`
  - `/reportes/encomiendas/` consume `vw_logistica_encomiendas`
  - `/dashboard/`: calcula totales simples para la pantalla principal mostrada.

## Estructura del Proyecto

El proyecto se organizara dentro de la carpeta `Proyecto final` de la siguiente forma:

- `backend/`: proyecto Django monolitico, conexion Oracle, modelos, formularios, vistas, templates y archivos static.
- `frontend/`: no se usara como aplicacion separada; se mantiene vacia o se elimina si no se necesita.
- Raiz del proyecto: archivos SQL, enunciado, imagen de referencia y documentacion general.

## Reglas de Integracion

- La logica de venta, registro de encomienda y finalizacion de viaje debe vivir en Oracle, no duplicarse en Django.
- Django solo validara campos basicos requeridos y traducira errores Oracle `RAISE_APPLICATION_ERROR` a mensajes claros en pantalla.
- Los inserts normales de CRUD deben respetar triggers y constraints existentes.
- Las vistas se consumiran como consultas de lectura; no tendran formularios de creacion, edicion ni eliminacion.
- Las contrasenas se mantendran segun la tabla actual para simplicidad universitaria, dejando documentado que en produccion deberian hashearse.
- No se usaran React, Vite, SPA, microservicios, JWT ni frontend desacoplado.

## Test Plan

- Probar conexion Django a Oracle.
- Validar login con usuario activo existente en `usuarios`.
- Probar CRUD completo de al menos un modulo exigido, recomendado: `autobuses` o `rutas`.
- Probar `sp_vender_boleto`:
  - venta exitosa;
  - asiento ocupado;
  - viaje no programado;
  - asiento fuera de capacidad.
- Probar `sp_registrar_encomienda`:
  - registro exitoso;
  - peso invalido;
  - remitente igual a destinatario;
  - viaje no programado.
- Probar `sp_finalizar_viaje`:
  - finalizacion exitosa;
  - viaje inexistente;
  - viaje ya finalizado.
- Probar reportes desde las 3 vistas.
- Verificar que los triggers respondan correctamente ante modificaciones no permitidas.
- Probar navegacion basica entre dashboard, CRUD, formularios transaccionales y reportes.

## Assumptions

- La base de datos objetivo es Oracle, porque el enunciado y los SQL usan PL/SQL, `VARCHAR2`, `SYSDATE`, `RAISE_APPLICATION_ERROR` e identity columns.
- La aplicacion Django sera el entregable principal en esta carpeta; el frontend se construira con templates dentro del mismo proyecto.
- No se usaran migraciones de Django para crear las tablas principales, porque la estructura ya existe en SQL.
- El codigo priorizara claridad academica sobre patrones empresariales avanzados.

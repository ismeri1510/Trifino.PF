-- ============================================================
-- VISTAS PARA REPORTES GERENCIALES
-- ============================================================

CREATE OR REPLACE VIEW vw_reporte_viajes AS
SELECT
    v.id_viaje,
    r.origen,
    r.destino,
    v.fecha_salida,
    v.hora_salida,
    v.fecha_fin,
    v.estado,
    a.placa,
    a.modelo,
    a.capacidad,
    p.nombre AS piloto,
    NVL(b.boletos_vendidos, 0) AS boletos_vendidos,
    a.capacidad - NVL(b.boletos_vendidos, 0) AS asientos_disponibles,
    NVL(b.ingresos_boletos, 0) AS ingresos_boletos,
    NVL(e.encomiendas_registradas, 0) AS encomiendas_registradas,
    NVL(e.ingresos_encomiendas, 0) AS ingresos_encomiendas,
    NVL(b.ingresos_boletos, 0) + NVL(e.ingresos_encomiendas, 0) AS ingresos_totales
FROM viajes v
INNER JOIN rutas r ON r.id_ruta = v.id_ruta
INNER JOIN autobuses a ON a.id_autobus = v.id_autobus
INNER JOIN pilotos p ON p.id_piloto = v.id_piloto
LEFT JOIN (
    SELECT
        id_viaje,
        COUNT(*) AS boletos_vendidos,
        SUM(precio) AS ingresos_boletos
    FROM boletos
    WHERE estado <> 'ANULADO'
    GROUP BY id_viaje
) b ON b.id_viaje = v.id_viaje
LEFT JOIN (
    SELECT
        id_viaje,
        COUNT(*) AS encomiendas_registradas,
        SUM(costo) AS ingresos_encomiendas
    FROM encomiendas
    GROUP BY id_viaje
) e ON e.id_viaje = v.id_viaje;
----------------------------------------------------------------
select * from vw_reporte_viajes
----------------------------------------------------------------

CREATE OR REPLACE VIEW vw_ocupacion_rutas AS
SELECT
    r.id_ruta,
    r.origen,
    r.destino,
    COUNT(v.id_viaje) AS total_viajes,
    SUM(a.capacidad) AS capacidad_total,
    NVL(SUM(b.boletos_vendidos), 0) AS boletos_vendidos,
    ROUND(
        CASE
            WHEN SUM(a.capacidad) > 0
            THEN (NVL(SUM(b.boletos_vendidos), 0) / SUM(a.capacidad)) * 100
            ELSE 0
        END,
        2
    ) AS porcentaje_ocupacion,
    NVL(SUM(b.ingresos_boletos), 0) AS ingresos_boletos
FROM rutas r
LEFT JOIN viajes v ON v.id_ruta = r.id_ruta
LEFT JOIN autobuses a ON a.id_autobus = v.id_autobus
LEFT JOIN (
    SELECT
        id_viaje,
        COUNT(*) AS boletos_vendidos,
        SUM(precio) AS ingresos_boletos
    FROM boletos
    WHERE estado <> 'ANULADO'
    GROUP BY id_viaje
) b ON b.id_viaje = v.id_viaje
GROUP BY r.id_ruta, r.origen, r.destino;

----------------------------------------------------------------
select * from vw_ocupacion_rutas;
----------------------------------------------------------------


CREATE OR REPLACE VIEW vw_logistica_encomiendas AS
SELECT
    e.id_encomienda,
    e.codigo_rastreo,
    rem.nombre AS remitente,
    dest.nombre AS destinatario,
    r.origen,
    r.destino,
    v.fecha_salida,
    v.hora_salida,
    e.peso,
    e.costo,
    e.estado,
    e.fecha_envio
FROM encomiendas e
INNER JOIN clientes_encomienda rem ON rem.id_cliente = e.id_remitente
INNER JOIN clientes_encomienda dest ON dest.id_cliente = e.id_destinatario
INNER JOIN viajes v ON v.id_viaje = e.id_viaje
INNER JOIN rutas r ON r.id_ruta = v.id_ruta;


---------------------------------------------------------------
select * from vw_logistica_encomiendas
---------------------------------------------------------------

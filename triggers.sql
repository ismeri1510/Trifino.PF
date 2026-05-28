--TRIGGERS
--triger 1 regla de negocio
--Si un viaje ya está: FINALIZADO, no se permiten cambios: piloto, bus, ruta, datos.

CREATE OR REPLACE TRIGGER trg_no_modificar_viaje_finalizado
BEFORE UPDATE ON viajes
FOR EACH ROW
BEGIN
    IF :OLD.estado = 'FINALIZADO' THEN
        RAISE_APPLICATION_ERROR(
            -20301,
            'No se puede modificar un viaje que ya fue finalizado.'
        );
    END IF;
END;
/

--PRUEBA: tiene que tirar error
UPDATE viajes
SET hora_salida = '11:00 AM'
WHERE id_viaje = 2;

--trigger 2 regla de negocio
--no se puede asignar un bus que ya tiene un viaje con la misma fecha y hora
CREATE OR REPLACE TRIGGER trg_validar_autobus_disponible
BEFORE INSERT ON viajes
FOR EACH ROW
DECLARE
    v_total NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_total
    FROM viajes
    WHERE id_autobus = :NEW.id_autobus
      AND fecha_salida = :NEW.fecha_salida
      AND hora_salida = :NEW.hora_salida
      AND estado = 'PROGRAMADO';

    IF v_total > 0 THEN
        RAISE_APPLICATION_ERROR(
            -20302,
            'El autobus ya tiene un viaje programado en esa fecha y hora.'
        );
    END IF;
END;
/


--prueba
INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (
    1,
    1,
    2,
    TO_DATE('2026-05-20','YYYY-MM-DD'),
    '08:00 AM',
    'PROGRAMADO'
);

--tendria que salir error y el mensaje de : el autobus ya tiene un viaje programado ...
--ver
select * from viajes

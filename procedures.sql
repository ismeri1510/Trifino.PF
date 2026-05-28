-- ============================================================
-- PROCEDIMIENTOS
-- ============================================================
---------------------------------------------------------------
--venta de boletos 
--existencia del pasajero
--existencia y estado del viaje
--capacidad del bus y disponibilidad del asiento
--asigna el precio desde la ruta, registra auditoria
---------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_vender_boleto (
    p_id_pasajero      IN boletos.id_pasajero%TYPE,
    p_id_viaje         IN boletos.id_viaje%TYPE,
    p_numero_asiento   IN boletos.numero_asiento%TYPE,
    p_usuario_sistema  IN auditoria.usuario_sistema%TYPE DEFAULT USER,
    p_id_boleto        OUT boletos.id_boleto%TYPE
) AS
    v_capacidad_autobus autobuses.capacidad%TYPE;
    v_precio_boleto rutas.precio_base%TYPE;
    v_estado_viaje viajes.estado%TYPE;
    v_total_pasajeros NUMBER;
    v_asientos_ocupados NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_total_pasajeros
    FROM pasajeros
    WHERE id_pasajero = p_id_pasajero;

    IF v_total_pasajeros = 0 THEN
        RAISE_APPLICATION_ERROR(-20001, 'El pasajero indicado no existe.');
    END IF;

    SELECT a.capacidad, r.precio_base, v.estado
    INTO v_capacidad_autobus, v_precio_boleto, v_estado_viaje
    FROM viajes v
    INNER JOIN autobuses a ON a.id_autobus = v.id_autobus
    INNER JOIN rutas r ON r.id_ruta = v.id_ruta
    WHERE v.id_viaje = p_id_viaje;

    IF v_estado_viaje <> 'PROGRAMADO' THEN
        RAISE_APPLICATION_ERROR(-20002, 'Solo se pueden vender boletos para viajes programados.');
    END IF;

    IF p_numero_asiento < 1 OR p_numero_asiento > v_capacidad_autobus THEN
        RAISE_APPLICATION_ERROR(-20003, 'El numero de asiento esta fuera de la capacidad del autobus.');
    END IF;

    SELECT COUNT(*)
    INTO v_asientos_ocupados
    FROM boletos
    WHERE id_viaje = p_id_viaje
      AND numero_asiento = p_numero_asiento
      AND estado <> 'ANULADO';

    IF v_asientos_ocupados > 0 THEN
        RAISE_APPLICATION_ERROR(-20004, 'El asiento ya esta vendido para este viaje.');
    END IF;

    INSERT INTO boletos (
        id_pasajero,
        id_viaje,
        numero_asiento,
        precio,
        estado
    )
    VALUES (
        p_id_pasajero,
        p_id_viaje,
        p_numero_asiento,
        v_precio_boleto,
        'CONFIRMADO'
    )
    RETURNING id_boleto INTO p_id_boleto;

    INSERT INTO auditoria (
        tabla_afectada,
        accion,
        usuario_sistema,
        descripcion
    )
    VALUES (
        'BOLETOS',
        'INSERT',
        p_usuario_sistema,
        'Venta de boleto ' || p_id_boleto || ' para viaje ' || p_id_viaje
    );

    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20005, 'El viaje indicado no existe.');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_vender_boleto;
/
----------------------------------------------------------
--registra encomiendas
--valida peso, clientes, viaje programado, calcula autom?ticamente el costo de env?o
--genera un c?digo ?nico de rastreo y deja evidencia en auditor?a
--==========================================================
CREATE OR REPLACE PROCEDURE sp_registrar_encomienda (
    p_id_remitente     IN encomiendas.id_remitente%TYPE,
    p_id_destinatario  IN encomiendas.id_destinatario%TYPE,
    p_id_viaje         IN encomiendas.id_viaje%TYPE,
    p_peso             IN encomiendas.peso%TYPE,
    p_descripcion      IN encomiendas.descripcion%TYPE,
    p_usuario_sistema  IN auditoria.usuario_sistema%TYPE DEFAULT USER,
    p_id_encomienda    OUT encomiendas.id_encomienda%TYPE,
    p_codigo_rastreo   OUT encomiendas.codigo_rastreo%TYPE
) AS
    v_total_clientes_validos NUMBER;
    v_estado_viaje viajes.estado%TYPE;
    v_costo_envio encomiendas.costo%TYPE;
BEGIN
    IF p_peso <= 0 THEN
        RAISE_APPLICATION_ERROR(-20101, 'El peso de la encomienda debe ser mayor que cero.');
    END IF;

    IF p_id_remitente = p_id_destinatario THEN
        RAISE_APPLICATION_ERROR(-20102, 'El remitente y destinatario no pueden ser el mismo cliente.');
    END IF;

    SELECT COUNT(*)
    INTO v_total_clientes_validos
    FROM clientes_encomienda
    WHERE id_cliente IN (p_id_remitente, p_id_destinatario);

    IF v_total_clientes_validos < 2 THEN
        RAISE_APPLICATION_ERROR(-20103, 'El remitente o destinatario no existe.');
    END IF;

    SELECT estado
    INTO v_estado_viaje
    FROM viajes
    WHERE id_viaje = p_id_viaje;

    IF v_estado_viaje <> 'PROGRAMADO' THEN
        RAISE_APPLICATION_ERROR(-20104, 'Solo se pueden registrar encomiendas en viajes programados.');
    END IF;

    v_costo_envio := 15 + (p_peso * 8);

    INSERT INTO encomiendas (
        id_remitente,
        id_destinatario,
        id_viaje,
        peso,
        descripcion,
        costo,
        estado
    )
    VALUES (
        p_id_remitente,
        p_id_destinatario,
        p_id_viaje,
        p_peso,
        p_descripcion,
        v_costo_envio,
        'PENDIENTE'
    )
    RETURNING id_encomienda INTO p_id_encomienda;

    p_codigo_rastreo := 'TRI' || LPAD(p_id_encomienda, 6, '0');

    UPDATE encomiendas
    SET codigo_rastreo = p_codigo_rastreo
    WHERE id_encomienda = p_id_encomienda;

    INSERT INTO auditoria (
        tabla_afectada,
        accion,
        usuario_sistema,
        descripcion
    )
    VALUES (
        'ENCOMIENDAS',
        'INSERT',
        p_usuario_sistema,
        'Registro de encomienda ' || p_codigo_rastreo || ' para viaje ' || p_id_viaje
    );

    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20105, 'El viaje indicado no existe.');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_registrar_encomienda;
/


-------------------------------------------------------
--permite finalizar un viaje
--valida que el viaje exista,
--que no haya sido finalizado antes y que la fecha final no sea menor que la fecha de salida
--actualiza el estado del viaje, libera el autob
--marca las encomendas del viaje como entregadas
--registra la acci?n en auditor?a
-------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_finalizar_viaje (
    p_id_viaje         IN viajes.id_viaje%TYPE,
    p_fecha_fin        IN viajes.fecha_fin%TYPE DEFAULT SYSDATE,
    p_usuario_sistema  IN auditoria.usuario_sistema%TYPE DEFAULT USER
) AS
    v_id_autobus_asignado viajes.id_autobus%TYPE;
    v_estado_actual_viaje viajes.estado%TYPE;
    v_fecha_salida_viaje viajes.fecha_salida%TYPE;
BEGIN
    SELECT id_autobus, estado, fecha_salida
    INTO v_id_autobus_asignado, v_estado_actual_viaje, v_fecha_salida_viaje
    FROM viajes
    WHERE id_viaje = p_id_viaje;

    IF v_estado_actual_viaje = 'FINALIZADO' THEN
        RAISE_APPLICATION_ERROR(-20201, 'El viaje ya se encuentra finalizado.');
    END IF;

    IF p_fecha_fin < v_fecha_salida_viaje THEN
        RAISE_APPLICATION_ERROR(-20202, 'La fecha de finalizacion no puede ser menor que la fecha de salida.');
    END IF;

    UPDATE viajes
    SET estado = 'FINALIZADO',
        fecha_fin = p_fecha_fin
    WHERE id_viaje = p_id_viaje;

    UPDATE autobuses
    SET estado = 'DISPONIBLE'
    WHERE id_autobus = v_id_autobus_asignado;

    UPDATE encomiendas
    SET estado = 'ENTREGADO'
    WHERE id_viaje = p_id_viaje
      AND estado IN ('PENDIENTE', 'EN TRANSITO');

    INSERT INTO auditoria (
        tabla_afectada,
        accion,
        usuario_sistema,
        descripcion
    )
    VALUES (
        'VIAJES',
        'UPDATE',
        p_usuario_sistema,
        'Finalizacion del viaje ' || p_id_viaje
    );

    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20203, 'El viaje indicado no existe.');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_finalizar_viaje;



/

-- ============================================================
-- prueabs
-- ============================================================

------------------- Venta de bleto -------------------
 VARIABLE v_id_boleto NUMBER;
 EXEC sp_vender_boleto(1, 2, 11, 'OPERADOR', :v_id_boleto);
 PRINT v_id_boleto;
 
select * from boletos 
select * from auditoria
------------------- ------------------- -------------------


------------------- Registro de encomienda -------------------
 VARIABLE v_id_encomienda NUMBER;
 VARIABLE v_codigo_rastreo VARCHAR2(50);
 EXEC sp_registrar_encomienda(1, 3, 2, 4.5, 'Sobre con documentos', 'OPERADOR', :v_id_encomienda, :v_codigo_rastreo);
 PRINT v_id_encomienda;
 PRINT v_codigo_rastreo;
 
 select * from encomiendas;
 select * from auditoria;

------------------- ------------------- ------------------- 

-------------------  Finalizacion de viaje ------------------- 
-- EXEC sp_finalizar_viaje(2, SYSDATE, 'OPERADOR');
EXEC sp_finalizar_viaje(2, TO_DATE('2026-05-21', 'YYYY-MM-DD'), 'OPERADOR');

 select * from boletos 
 select * from encomiendas;
 select * from auditoria;
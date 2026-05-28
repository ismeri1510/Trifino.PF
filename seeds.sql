--inserts de las tablas


--USUARIOS
INSERT INTO usuarios (nombre, correo, password, rol, estado)
VALUES ('Administrador General', 'admin@trifinio.com', 'admin123', 'ADMIN', 'ACTIVO');

INSERT INTO usuarios (nombre, correo, password, rol, estado)
VALUES ('Operador Central', 'operador@trifinio.com', 'operador123', 'OPERADOR', 'ACTIVO');
SELECT * FROM usuarios;

--BUSES
INSERT INTO autobuses (placa, modelo, capacidad, estado)
VALUES ('C-123ABC', 'Mercedes Benz 2020', 40, 'DISPONIBLE');

INSERT INTO autobuses (placa, modelo, capacidad, estado)
VALUES ('C-456DEF', 'Volvo 2019', 45, 'DISPONIBLE');

INSERT INTO autobuses (placa, modelo, capacidad, estado)
VALUES ('C-789GHI', 'Hyundai Universe', 50, 'MANTENIMIENTO');

INSERT INTO autobuses (placa, modelo, capacidad, estado)
VALUES ('C-321JKL', 'Scania Touring', 42, 'DISPONIBLE');

INSERT INTO autobuses (placa, modelo, capacidad, estado)
VALUES ('C-654MNO', 'Marcopolo Paradiso', 48, 'EN VIAJE');

SELECT * FROM autobuses;

--PILOTOS
INSERT INTO pilotos (nombre, dpi, telefono, licencia, estado)
VALUES ('Carlos Hernández', '3012456780101', '4587-1234', 'LIC-A001', 'ACTIVO');

INSERT INTO pilotos (nombre, dpi, telefono, licencia, estado)
VALUES ('José Ramírez', '2876543210102', '5123-9876', 'LIC-A002', 'ACTIVO');

INSERT INTO pilotos (nombre, dpi, telefono, licencia, estado)
VALUES ('Miguel López', '3154789650103', '4765-1122', 'LIC-A003', 'VACACIONES');

INSERT INTO pilotos (nombre, dpi, telefono, licencia, estado)
VALUES ('Fernando García', '2987456120104', '4899-4455', 'LIC-A004', 'ACTIVO');

INSERT INTO pilotos (nombre, dpi, telefono, licencia, estado)
VALUES ('Luis Martínez', '3245789010105', '5566-7788', 'LIC-A005', 'INACTIVO');

SELECT * FROM pilotos;

--RUTAS
INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Chiquimula', 'Ciudad de Guatemala', 175, 85.00, '4 horas');

INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Zacapa', 'Esquipulas', 95, 45.00, '2 horas');

INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Ciudad de Guatemala', 'Jutiapa', 145, 70.00, '3.5 horas');

INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Esquipulas', 'San Salvador', 210, 120.00, '5 horas');

INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Chiquimula', 'Copán Ruinas', 130, 95.00, '3 horas');

INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Jalapa', 'Ciudad de Guatemala', 105, 55.00, '2.5 horas');

INSERT INTO rutas (origen, destino, distancia_km, precio_base, duracion)
VALUES ('Puerto Barrios', 'Zacapa', 220, 110.00, '5 horas');

SELECT * FROM rutas;

--PASAJEROS
INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Ana López', '3011122230101', '5511-2233', 'ana.lopez@gmail.com');

INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Mario Pérez', '2877766650102', '4455-6677', 'mario.perez@gmail.com');

INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Lucía Hernández', '3155544430103', '5122-3344', 'lucia.h@gmail.com');

INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Daniel Ramírez', '2988877760104', '4788-9900', 'daniel.r@gmail.com');

INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Sofía Martínez', '3244411120105', '5666-1122', 'sofia.m@gmail.com');

INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Kevin García', '3019998880106', '4333-2211', 'kevin.g@gmail.com');

INSERT INTO pasajeros (nombre, dpi, telefono, correo)
VALUES ('Andrea Morales', '2871234560107', '5777-8899', 'andrea.m@gmail.com');

SELECT * FROM pasajeros;

--CLIENTES ENCOMIENDAS
INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('Roberto Castillo', '5512-7788', 'Chiquimula, Zona 1', '3011111110101');

INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('Patricia Gómez', '4422-8899', 'Zacapa, Barrio Las Flores', '2872222220102');

INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('Esteban Morales', '5333-6677', 'Esquipulas, Zona 2', '3153333330103');

INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('Claudia Hernández', '4888-1122', 'Jutiapa, Centro', '2984444440104');

INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('Jorge Pérez', '5666-9900', 'Ciudad de Guatemala, Zona 18', '3245555550105');

INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('María López', '4555-3344', 'Puerto Barrios, Izabal', '3016666660106');

INSERT INTO clientes_encomienda (nombre, telefono, direccion, dpi)
VALUES ('Ricardo García', '5777-2211', 'Copán Ruinas, Honduras', '2877777770107');

SELECT * FROM clientes_encomienda;

--Tabla viajes
INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (1, 1, 1, TO_DATE('2026-05-20','YYYY-MM-DD'), '08:00 AM', 'PROGRAMADO');

INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (2, 2, 2, TO_DATE('2026-05-21','YYYY-MM-DD'), '09:30 AM', 'PROGRAMADO');

INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (3, 4, 4, TO_DATE('2026-05-22','YYYY-MM-DD'), '06:45 AM', 'PROGRAMADO');

INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (4, 1, 2, TO_DATE('2026-05-23','YYYY-MM-DD'), '10:15 AM', 'PROGRAMADO');

INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (5, 2, 1, TO_DATE('2026-05-24','YYYY-MM-DD'), '01:00 PM', 'PROGRAMADO');

INSERT INTO viajes (
    id_ruta,
    id_autobus,
    id_piloto,
    fecha_salida,
    hora_salida,
    estado
)
VALUES (6, 4, 4, TO_DATE('2026-05-25','YYYY-MM-DD'), '07:20 AM', 'FINALIZADO');

SELECT * FROM viajes;

--tabla boletos
INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (1, 1, 5, 85.00, 'CONFIRMADO');

INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (2, 1, 6, 85.00, 'CONFIRMADO');

INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (3, 2, 10, 45.00, 'CONFIRMADO');

INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (4, 3, 3, 70.00, 'CONFIRMADO');

INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (5, 4, 15, 120.00, 'CONFIRMADO');

INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (6, 5, 8, 95.00, 'CONFIRMADO');

INSERT INTO boletos (
    id_pasajero,
    id_viaje,
    numero_asiento,
    precio,
    estado
)
VALUES (7, 6, 12, 55.00, 'CONFIRMADO');

SELECT * FROM boletos;

--encomiendas
INSERT INTO encomiendas (
    id_remitente,
    id_destinatario,
    id_viaje,
    peso,
    descripcion,
    costo,
    codigo_rastreo,
    estado
)
VALUES (1, 2, 1, 5.5, 'Caja de documentos', 35.00, 'TRI001', 'EN TRANSITO');

INSERT INTO encomiendas (
    id_remitente,
    id_destinatario,
    id_viaje,
    peso,
    descripcion,
    costo,
    codigo_rastreo,
    estado
)
VALUES (3, 4, 2, 12.0, 'Paquete de ropa', 60.00, 'TRI002', 'PENDIENTE');

INSERT INTO encomiendas (
    id_remitente,
    id_destinatario,
    id_viaje,
    peso,
    descripcion,
    costo,
    codigo_rastreo,
    estado
)
VALUES (5, 6, 3, 8.3, 'Electrodoméstico pequeño', 75.00, 'TRI003', 'ENTREGADO');

INSERT INTO encomiendas (
    id_remitente,
    id_destinatario,
    id_viaje,
    peso,
    descripcion,
    costo,
    codigo_rastreo,
    estado
)
VALUES (2, 1, 4, 3.2, 'Medicamentos', 25.00, 'TRI004', 'EN TRANSITO');

INSERT INTO encomiendas (
    id_remitente,
    id_destinatario,
    id_viaje,
    peso,
    descripcion,
    costo,
    codigo_rastreo,
    estado
)
VALUES (4, 7, 5, 15.7, 'Herramientas', 90.00, 'TRI005', 'PENDIENTE');

INSERT INTO encomiendas (
    id_remitente,
    id_destinatario,
    id_viaje,
    peso,
    descripcion,
    costo,
    codigo_rastreo,
    estado
)
VALUES (6, 3, 6, 6.8, 'Libros universitarios', 40.00, 'TRI006', 'ENTREGADO');

SELECT * FROM encomiendas;

--tabla de MANTENIMIENTOS
INSERT INTO mantenimientos (
    id_autobus,
    fecha,
    descripcion,
    costo,
    tipo
)
VALUES (
    1,
    TO_DATE('2026-05-10','YYYY-MM-DD'),
    'Cambio de aceite y revisión general',
    850.00,
    'PREVENTIVO'
);

INSERT INTO mantenimientos (
    id_autobus,
    fecha,
    descripcion,
    costo,
    tipo
)
VALUES (
    2,
    TO_DATE('2026-05-12','YYYY-MM-DD'),
    'Reparación de frenos',
    1500.00,
    'CORRECTIVO'
);

INSERT INTO mantenimientos (
    id_autobus,
    fecha,
    descripcion,
    costo,
    tipo
)
VALUES (
    3,
    TO_DATE('2026-05-14','YYYY-MM-DD'),
    'Cambio de llantas',
    3200.00,
    'PREVENTIVO'
);

INSERT INTO mantenimientos (
    id_autobus,
    fecha,
    descripcion,
    costo,
    tipo
)
VALUES (
    4,
    TO_DATE('2026-05-15','YYYY-MM-DD'),
    'Revisión eléctrica',
    975.00,
    'CORRECTIVO'
);

INSERT INTO mantenimientos (
    id_autobus,
    fecha,
    descripcion,
    costo,
    tipo
)
VALUES (
    5,
    TO_DATE('2026-05-16','YYYY-MM-DD'),
    'Mantenimiento de motor',
    4500.00,
    'CORRECTIVO'
);

SELECT * FROM mantenimientos;

--auditoria 
INSERT INTO auditoria (
    tabla_afectada,
    accion,
    usuario_sistema,
    descripcion
)
VALUES (
    'BOLETOS',
    'INSERT',
    'ADMIN',
    'Se registró un nuevo boleto para el viaje 1'
);

INSERT INTO auditoria (
    tabla_afectada,
    accion,
    usuario_sistema,
    descripcion
)
VALUES (
    'ENCOMIENDAS',
    'INSERT',
    'OPERADOR',
    'Se registró una nueva encomienda con código TRI003'
);

SELECT * FROM auditoria;
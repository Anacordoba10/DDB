CREATE DATABASE DDB;

CREATE TABLE clientes (
    cedula VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    whatsapp VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE pedidos (
    numero_identificador VARCHAR(36) PRIMARY KEY,
    cantidad_hamburguesas INT NOT NULL,
    monto_delivery DECIMAL(10, 2) NOT NULL,
    total_pagar DECIMAL(10, 2) NOT NULL,
    modo_pago VARCHAR(50) NOT NULL,
    screenshot_pago VARCHAR(100),
    status VARCHAR(20) NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    ciudad VARCHAR(100),
    municipio VARCHAR(100),
    cedula_cliente VARCHAR(20),
    observaciones TEXT,
    FOREIGN KEY (cedula_cliente) REFERENCES clientes(cedula)
);

-- ============================================================
-- Schema del Sistema de Gestión de Inventario
-- ============================================================

-- Tabla de categorías de productos
CREATE TABLE categorias (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    nombre      NVARCHAR(100)  NOT NULL,
    descripcion NVARCHAR(255)  NULL,
    creado_en   DATETIME       NOT NULL DEFAULT GETDATE()
);

-- Tabla principal de productos
CREATE TABLE productos (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    nombre          NVARCHAR(150)  NOT NULL,
    descripcion     NVARCHAR(500)  NULL,
    precio          DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    stock           INT            NOT NULL DEFAULT 0,
    stock_minimo    INT            NOT NULL DEFAULT 5,  -- alerta de bajo stock
    categoria_id    INT            NULL,
    creado_en       DATETIME       NOT NULL DEFAULT GETDATE(),
    actualizado_en  DATETIME       NOT NULL DEFAULT GETDATE(),

    CONSTRAINT fk_producto_categoria
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        ON DELETE SET NULL  -- si se borra la categoría, el producto queda sin categoría
);

-- Tabla de movimientos de inventario (entradas y salidas)
CREATE TABLE movimientos (
    id           INT IDENTITY(1,1) PRIMARY KEY,
    producto_id  INT            NOT NULL,
    tipo         NVARCHAR(10)   NOT NULL CHECK (tipo IN ('entrada', 'salida')),
    cantidad     INT            NOT NULL CHECK (cantidad > 0),
    descripcion  NVARCHAR(255)  NULL,
    fecha        DATETIME       NOT NULL DEFAULT GETDATE(),

    CONSTRAINT fk_movimiento_producto
        FOREIGN KEY (producto_id) REFERENCES productos(id)
        ON DELETE CASCADE  -- si se borra el producto, se borran sus movimientos
);

-- Datos de prueba: categorías iniciales
INSERT INTO categorias (nombre, descripcion) VALUES
    ('Electrónica',   'Dispositivos y accesorios electrónicos'),
    ('Herramientas',  'Herramientas manuales y eléctricas'),
    ('Oficina',       'Artículos de papelería y oficina');

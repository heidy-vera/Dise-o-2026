-- ==========================================
-- BASE DE DATOS DULCES DELICIAS
-- SEMANA 13
-- ==========================================

CREATE DATABASE IF NOT EXISTS dulces_delicias;

USE dulces_delicias;


-- ==========================================
-- TABLA DE PROVEEDORES
-- ==========================================

CREATE TABLE IF NOT EXISTS proveedores (

    id INT AUTO_INCREMENT PRIMARY KEY,

    empresa VARCHAR(100) NOT NULL,

    producto VARCHAR(100) NOT NULL,

    telefono VARCHAR(20) NOT NULL,

    email VARCHAR(100) NOT NULL

);


-- ==========================================
-- TABLA DE PRODUCTOS
-- ==========================================

CREATE TABLE IF NOT EXISTS productos (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT NOT NULL,

    precio DECIMAL(10,2) NOT NULL,

    stock INT NOT NULL,

    imagen VARCHAR(100),

    icono VARCHAR(20),

    proveedor_id INT NULL,

    CONSTRAINT fk_productos_proveedor

        FOREIGN KEY (proveedor_id)

        REFERENCES proveedores(id)

);


-- ==========================================
-- TABLA DE CLIENTES
-- ==========================================

CREATE TABLE IF NOT EXISTS clientes (

    id INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    correo VARCHAR(100) NOT NULL,

    telefono VARCHAR(20) NOT NULL

);


-- ==========================================
-- TABLA DE FACTURAS
-- ==========================================

CREATE TABLE IF NOT EXISTS facturas (

    id INT AUTO_INCREMENT PRIMARY KEY,

    numero_factura VARCHAR(50) NOT NULL,

    cliente VARCHAR(100) NOT NULL,

    fecha DATE NOT NULL,

    producto VARCHAR(100) NOT NULL,

    cantidad INT NOT NULL,

    precio DECIMAL(10,2) NOT NULL,

    subtotal DECIMAL(10,2) NOT NULL,

    iva DECIMAL(10,2) NOT NULL,

    total DECIMAL(10,2) NOT NULL,

    estado VARCHAR(50) NOT NULL

);

-- ==========================================
-- USUARIOS
-- SEMANA 14
-- ==========================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
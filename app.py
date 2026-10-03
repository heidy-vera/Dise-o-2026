from flask import Flask, render_template, redirect, url_for, flash
import sqlite3
import os

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DE FLASK-WTF Y CSRF
# ==========================================
app.config["SECRET_KEY"] = "dulces-delicias-clave-secreta-2026"


# ==========================================
# CONFIGURACIÓN DE SQLITE
# ==========================================

DATABASE = os.path.join("data", "dulces_delicias.db")


def conectar_bd():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla_productos():

    # Crear carpeta data si no existe
    os.makedirs("data", exist_ok=True)

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            imagen TEXT,
            icono TEXT
        )
    """)

    conn.commit()
    conn.close()
def insertar_productos_iniciales():

    conn = conectar_bd()
    cursor = conn.cursor()

    productos = [
        (
            "Pasteles",
            "Pasteles personalizados para cumpleaños, bodas y eventos especiales.",
            20.00,
            8,
            "pastel.jpg",
            "🎂"
        ),
        (
            "Cupcakes",
            "Cupcakes decorados con diferentes sabores y diseños.",
            2.50,
            15,
            "cupcakes.jpg",
            "🧁"
        ),
        (
            "Galletas",
            "Galletas artesanales con sabores tradicionales.",
            1.50,
            20,
            "galletas.jpg",
            "🍪"
        ),
        (
            "Brownies",
            "Brownies suaves con chocolate y diferentes toppings.",
            3.00,
            10,
            "brownies.jpg",
            "🍫"
        ),
        (
            "Cheesecake",
            "Cheesecake cremoso con frutas y sabores especiales.",
            15.00,
            0,
            "cheesecake.jpg",
            "🍰"
        ),
        (
            "Donas",
            "Donas decoradas con chocolate, azúcar y diferentes sabores.",
            2.00,
            12,
            "donas.jpg",
            "🍩"
        )
    ]

    for producto in productos:

        cursor.execute("""
            SELECT id
            FROM productos
            WHERE nombre = ?
        """, (producto[0],))

        existe = cursor.fetchone()

        if not existe:

            cursor.execute("""
                INSERT INTO productos
                (nombre, descripcion, precio, stock, imagen, icono)
                VALUES (?, ?, ?, ?, ?, ?)
            """, producto)

    conn.commit()
    conn.close()
def crear_tabla_clientes():

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
def crear_tabla_proveedores():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            producto TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close() 
def crear_tabla_facturas():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_factura TEXT NOT NULL,
            cliente TEXT NOT NULL,
            fecha TEXT NOT NULL,
            total REAL NOT NULL,
            estado TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
def actualizar_tabla_facturas():

    conn = conectar_bd()
    cursor = conn.cursor()

    columnas = [
        ("producto", "TEXT"),
        ("cantidad", "INTEGER"),
        ("precio", "REAL"),
        ("subtotal", "REAL"),
        ("iva", "REAL")
    ]

    for nombre, tipo in columnas:

        try:
            cursor.execute(
                f"ALTER TABLE facturas ADD COLUMN {nombre} {tipo}"
            )
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()
# ==========================================
# PÁGINA PRINCIPAL
# ==========================================
@app.route("/")
def inicio():

    nombre_negocio = "Dulces Delicias"
    mensaje = "Bienvenidos a nuestra pastelería"

    return render_template(
        "index.html",
        nombre_negocio=nombre_negocio,
        mensaje=mensaje
    )
# ==========================================
# MÓDULO DE PRODUCTOS
# ==========================================
@app.route("/productos")
def productos():

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, precio, stock, imagen, icono
        FROM productos
    """)

    productos_lista = cursor.fetchall()

    conn.close()

    return render_template(
        "productos.html",
        productos=productos_lista
    )

# ==========================================
# FORMULARIO DE PRODUCTOS
# ==========================================
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio, stock, imagen, icono)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            "nuevos.jpg",
            "🥞"
        ))

        conn.commit()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================
# MÓDULO DE CLIENTES
# ==========================================
@app.route("/clientes")
def clientes():

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, correo, telefono
        FROM clientes
    """)

    clientes_lista = cursor.fetchall()

    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes_lista
    )

# ==========================================
# FORMULARIO DE CLIENTES
# ==========================================
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, correo, telefono)
            VALUES (?, ?, ?)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data
        ))

        conn.commit()
        conn.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# ==========================================
# MÓDULO DE PROVEEDORES
# ==========================================
@app.route("/proveedores")
def proveedores():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, empresa, producto, telefono, email
        FROM proveedores
    """)

    proveedores_lista = cursor.fetchall()

    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista
    )
# ==========================================
# FORMULARIO DE PROVEEDORES
# ==========================================
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (empresa, producto, telefono, email)
            VALUES (?, ?, ?, ?)
        """, (
            form.empresa.data,
            form.producto.data,
            form.telefono.data,
            form.email.data
        ))

        conn.commit()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

# ==========================================
# MÓDULO DE FACTURACIÓN
# ==========================================
@app.route("/facturacion")
def facturacion():

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            numero_factura,
            cliente,
            fecha,
            producto,
            cantidad,
            precio,
            subtotal,
            iva,
            total,
            estado
        FROM facturas
        ORDER BY id DESC
    """)

    facturacion_lista = cursor.fetchall()

    conn.close()

    return render_template(
        "facturacion_lista.html",
        facturas=facturacion_lista
    )
# ==========================================
# FORMULARIO DE FACTURACIÓN
# ==========================================
@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        subtotal = form.precio.data * form.cantidad.data

        # IVA del 15%
        iva = subtotal * 0.15

        # Total de la factura
        total = subtotal + iva


        # ==========================================
        # GUARDAR EN SQLITE
        # ==========================================

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (
                numero_factura,
                cliente,
                fecha,
                producto,
                cantidad,
                precio,
                subtotal,
                iva,
                total,
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            form.numero_factura.data,
            form.cliente.data,
            form.fecha.data.strftime("%Y-%m-%d"),
            form.producto.data,
            form.cantidad.data,
            form.precio.data,
            subtotal,
            iva,
            total,
            form.estado.data
        ))

        conn.commit()
        conn.close()


        # ==========================================
        # MENSAJE DE CONFIRMACIÓN
        # ==========================================

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))


    return render_template(
        "facturacion.html",
        form=form
    )
# ==========================================
# INICIALIZAR BASE DE DATOS
# ==========================================
crear_tabla_productos()
insertar_productos_iniciales()
crear_tabla_clientes()
crear_tabla_proveedores()
crear_tabla_facturas()
actualizar_tabla_facturas()

# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for, flash, request
from conexion.conexion import conectar_bd

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

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    # Consulta relacionada entre productos y proveedores
    cursor.execute("""
        SELECT
            productos.id,
            productos.nombre,
            productos.descripcion,
            productos.precio,
            productos.stock,
            productos.imagen,
            productos.icono,
            proveedores.empresa AS proveedor
        FROM productos
        LEFT JOIN proveedores
            ON productos.proveedor_id = proveedores.id
    """)

    productos_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

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

        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos
            (
                nombre,
                descripcion,
                precio,
                stock,
                imagen,
                icono
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            "nuevos.jpg",
            "🥞"
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

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
# MODIFICAR PRODUCTOS
# ==========================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    # Buscar el producto por ID
    cursor.execute("""
        SELECT
            id,
            nombre,
            descripcion,
            precio,
            stock
        FROM productos
        WHERE id = %s
    """, (id,))

    producto = cursor.fetchone()

    # Si el producto no existe
    if not producto:

        cursor.close()
        conexion.close()

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(url_for("productos"))

    form = ProductoForm()

    # Cuando se envía el formulario
    if form.validate_on_submit():

        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                stock = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.precio.data,
            form.stock.data,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Producto modificado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    # Cuando se abre el formulario
    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    cursor.close()
    conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Editar producto"
    )


# ==========================================
# ELIMINAR PRODUCTOS
# ==========================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id = %s
    """, (id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect(url_for("productos"))


# ==========================================
# MÓDULO DE CLIENTES
# ==========================================

@app.route("/clientes")
def clientes():

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nombre,
            correo,
            telefono
        FROM clientes
    """)

    clientes_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

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

        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (
                nombre,
                correo,
                telefono
            )
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.correo.data,
            form.telefono.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

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

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            empresa,
            producto,
            telefono,
            email
        FROM proveedores
    """)

    proveedores_lista = cursor.fetchall()

    cursor.close()
    conexion.close()

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

        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (
                empresa,
                producto,
                telefono,
                email
            )
            VALUES (%s, %s, %s, %s)
        """, (
            form.empresa.data,
            form.producto.data,
            form.telefono.data,
            form.email.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

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

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

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

    cursor.close()
    conexion.close()

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

        # ==========================================
        # CÁLCULO DEL SUBTOTAL
        # ==========================================

        subtotal = form.precio.data * form.cantidad.data

        # ==========================================
        # CÁLCULO DEL IVA DEL 15%
        # ==========================================

        iva = subtotal * 0.15

        # ==========================================
        # CÁLCULO DEL TOTAL
        # ==========================================

        total = subtotal + iva

        # ==========================================
        # GUARDAR EN MYSQL
        # ==========================================

        conexion = conectar_bd()
        cursor = conexion.cursor()

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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            form.numero_factura.data,
            form.cliente.data,
            form.fecha.data,
            form.producto.data,
            form.cantidad.data,
            form.precio.data,
            subtotal,
            iva,
            total,
            form.estado.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

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
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)

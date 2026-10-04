from flask import Flask, render_template, redirect, url_for, flash, request

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import conectar_bd

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

from models import Usuario


app = Flask(__name__)

app.config["SECRET_KEY"] = "dulces-delicias-clave-secreta-2026"

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):

    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"]
        )

    return None
# ==========================================
# REGISTRO DE USUARIOS
# ==========================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # Comprobar si el usuario ya existe
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conexion.close()

            flash(
                "El nombre de usuario ya existe.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Proteger la contraseña mediante hash
        password_hash = generate_password_hash(
            form.password.data
        )

        # Registrar usuario
        cursor.execute("""
            INSERT INTO usuarios
            (
                usuario,
                password
            )
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )
# ==========================================
# INICIO DE SESIÓN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    print("--------------------------------")
    print("ENTRANDO A LOGIN")
    print("METODO:", request.method)
    print("USUARIO RECIBIDO:", form.usuario.data)
    print("FORMULARIO VALIDO:", form.validate_on_submit())
    print("ERRORES DEL FORMULARIO:", form.errors)
    print("--------------------------------")

    if form.validate_on_submit():

        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                usuario,
                password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        print("USUARIO EN MYSQL:", usuario)

        if usuario is None:

            flash(
                "El usuario no existe.",
                "danger"
            )

            return render_template(
                "login.html",
                form=form
            )

        if not check_password_hash(
            usuario["password"],
            form.password.data
        ):

            print("LA CONTRASEÑA NO COINCIDE")

            flash(
                "La contraseña es incorrecta.",
                "danger"
            )

            return render_template(
                "login.html",
                form=form
            )

        usuario_obj = Usuario(
            usuario["id"],
            usuario["usuario"]
        )

        login_user(usuario_obj)

        print("================================")
        print("LOGIN CORRECTO")
        print("ID:", usuario_obj.id)
        print("USUARIO:", usuario_obj.usuario)
        print("AUTENTICADO:", current_user.is_authenticated)
        print("================================")

        flash(
            "Inicio de sesión exitoso.",
            "success"
        )

        return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        form=form
    )
# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==========================================
# CERRAR SESIÓN
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

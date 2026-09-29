from flask import Flask, render_template, redirect, url_for, flash

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
# DATOS TEMPORALES
# ==========================================

productos_lista = [
    {
        "nombre": "Pasteles",
        "descripcion": "Pasteles personalizados para cumpleaños, bodas y eventos especiales.",
        "precio": 20.00,
        "stock": 8,
        "imagen": "pastel.jpg",
        "icono": "🎂"
    },
    {
        "nombre": "Cupcakes",
        "descripcion": "Cupcakes decorados con diferentes sabores y diseños.",
        "precio": 2.50,
        "stock": 15,
        "imagen": "cupcakes.jpg",
        "icono": "🧁"
    },
    {
        "nombre": "Galletas",
        "descripcion": "Galletas artesanales con sabores tradicionales.",
        "precio": 1.50,
        "stock": 20,
        "imagen": "galletas.jpg",
        "icono": "🍪"
    },
    {
        "nombre": "Brownies",
        "descripcion": "Brownies suaves con chocolate y diferentes toppings.",
        "precio": 3.00,
        "stock": 10,
        "imagen": "brownies.jpg",
        "icono": "🍫"
    },
    {
        "nombre": "Cheesecake",
        "descripcion": "Cheesecake cremoso con frutas y sabores especiales.",
        "precio": 15.00,
        "stock": 0,
        "imagen": "cheesecake.jpg",
        "icono": "🍰"
    },
    {
        "nombre": "Donas",
        "descripcion": "Donas decoradas con chocolate, azúcar y diferentes sabores.",
        "precio": 2.00,
        "stock": 12,
        "imagen": "donas.jpg",
        "icono": "🍩"
    }
]


clientes_lista = [
    {
        "nombre": "María López",
        "telefono": "0991234567",
        "correo": "maria@gmail.com"
    },
    {
        "nombre": "Juan Pérez",
        "telefono": "0987654321",
        "correo": "juan@gmail.com"
    },
    {
        "nombre": "Ana Torres",
        "telefono": "0976543210",
        "correo": "ana@gmail.com"
    }
]


proveedores_lista = [
    {
        "nombre": "Distribuidora La Esperanza",
        "producto": "Harina",
        "telefono": "0991112233",
        "correo": "esperanza@gmail.com"
    },
    {
        "nombre": "Lácteos Andinos",
        "producto": "Leche y queso",
        "telefono": "0982223344",
        "correo": "lacteos@gmail.com"
    },
    {
        "nombre": "Frutas del Valle",
        "producto": "Frutas",
        "telefono": "0973334455",
        "correo": "frutas@gmail.com"
    }
]

facturas = []


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

        nuevo = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "precio": form.precio.data,
            "stock": form.stock.data,
            "imagen": "pastel.jpg",
            "icono": "🎂"
        }

        productos_lista.append(nuevo)

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

        nuevo = {
            "nombre": form.nombre.data,
            "telefono": form.telefono.data,
            "correo": form.correo.data
        }

        clientes_lista.append(nuevo)

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

        nuevo = {
            "nombre": form.empresa.data,
            "producto": form.producto.data,
            "telefono": form.telefono.data,
            "correo": form.email.data
        }

        proveedores_lista.append(nuevo)

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

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# ==========================================
# FORMULARIO DE FACTURACIÓN
# ==========================================
@app.route("/facturacion/nueva", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva = {
            "numero_factura": form.numero_factura.data,
            "cliente": form.cliente.data,
            "fecha": form.fecha.data,
            "total": form.total.data,
            "estado": form.estado.data
        }

        facturas.append(nueva)

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)
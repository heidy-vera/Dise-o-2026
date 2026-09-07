from flask import Flask, render_template

app = Flask(__name__)


# =========================
# PÁGINA PRINCIPAL
# =========================
@app.route("/")
def inicio():

    nombre_negocio = "Dulces Delicias"
    mensaje = "Bienvenidos a nuestra pastelería"

    return render_template(
        "index.html",
        nombre_negocio=nombre_negocio,
        mensaje=mensaje
    )


# =========================
# MÓDULO DE PRODUCTOS
# =========================
@app.route("/productos")
def productos():

    productos = [
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

    return render_template(
        "productos.html",
        productos=productos
    )

# =========================
# MÓDULO DE CLIENTES
# =========================
@app.route("/clientes")
def clientes():

    clientes = [
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

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# =========================
# MÓDULO DE PROVEEDORES
# =========================
@app.route("/proveedores")
def proveedores():

    proveedores = [
        {
            "nombre": "Distribuidora La Esperanza",
            "producto": "Harina",
            "telefono": "0991112233"
        },
        {
            "nombre": "Lácteos Andinos",
            "producto": "Leche y queso",
            "telefono": "0982223344"
        },
        {
            "nombre": "Frutas del Valle",
            "producto": "Frutas",
            "telefono": "0973334455"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# =========================
# MÓDULO DE FACTURACIÓN
# =========================
@app.route("/facturacion")
def facturacion():

    return render_template("facturacion.html")


# =========================
# EJECUTAR APLICACIÓN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
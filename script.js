// ==========================
// PRODUCTOS DINÁMICOS
// ==========================

const productos = [
    {
        nombre: "Torta Personalizada",
        descripcion: "Diseñadas para cumpleaños, bodas y ocasiones especiales.",
        imagen: "img/pastel.jpg",
        emoji: "🎂"
    },
    {
        nombre: "Cupcakes",
        descripcion: "Deliciosos cupcakes con diferentes sabores y decoraciones.",
        imagen: "img/cupcakes.jpg",
        emoji: "🧁"
    },
    {
        nombre: "Brownies",
        descripcion: "Brownies artesanales preparados con ingredientes de alta calidad.",
        imagen: "img/brownies.jpg",
        emoji: "🍫"
    },
    {
        nombre: "Cheesecakes",
        descripcion: "Cheesecakes cremosos con diferentes sabores y coberturas.",
        imagen: "img/cheesecake.jpg",
        emoji: "🍰"
    },
    {
        nombre: "Galletas Artesanales",
        descripcion: "Galletas elaboradas con ingredientes naturales y sabores únicos.",
        imagen: "img/galletas.jpg",
        emoji: "🍪"
    },
    {
        nombre: "Donas",
        descripcion: "Donas esponjosas con diferentes glaseados y decoraciones.",
        imagen: "img/donas.jpg",
        emoji: "🍩"
    }
];

// Mostrar productos

function cargarProductos() {

    const lista = document.getElementById("listaProductos");

    if (!lista) return;

    lista.innerHTML = "";

    // Condición solicitada
    if (productos.length === 0) {

        lista.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning text-center">
                    No existen productos registrados.
                </div>
            </div>
        `;

        return;
    }

    // Estructura repetitiva
    productos.forEach(producto => {

        lista.innerHTML += `

        <div class="col-md-4">

            <div class="card shadow m-3 h-100">

                <img
                    src="${producto.imagen}"
                    class="card-img-top"
                    alt="${producto.nombre}">

                <div class="card-body text-center">

                    <h4>${producto.emoji} ${producto.nombre}</h4>

                    <p>${producto.descripcion}</p>

                    <button class="btn btn-outline-danger">
                        Comprar
                    </button>

                </div>

            </div>

        </div>

        `;

    });

}

// Cargar productos al abrir la página
cargarProductos();

// ==========================
// FORMULARIO DE PEDIDOS
// ==========================

// Obtener elementos

const formulario = document.getElementById("formPedido");

const cliente = document.getElementById("cliente");
const producto = document.getElementById("producto");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const listaPedidos = document.getElementById("listaPedidos");
const contador = document.getElementById("contador");
const mensaje = document.getElementById("mensaje");

// Arreglo de pedidos

let pedidos = [];

// ==========================
// VALIDACIONES
// ==========================

function validarCliente() {

    if (cliente.value.trim() === "") {

        cliente.classList.remove("is-valid");
        cliente.classList.add("is-invalid");

        document.getElementById("errorCliente").textContent =
            "El nombre es obligatorio.";

        return false;
    }

    if (cliente.value.trim().length < 3) {

        cliente.classList.remove("is-valid");
        cliente.classList.add("is-invalid");

        document.getElementById("errorCliente").textContent =
            "Debe tener al menos 3 caracteres.";

        return false;
    }

    cliente.classList.remove("is-invalid");
    cliente.classList.add("is-valid");

    return true;
}

function validarProducto() {

    if (producto.value.trim() === "") {

        producto.classList.remove("is-valid");
        producto.classList.add("is-invalid");

        document.getElementById("errorProducto").textContent =
            "Ingrese un producto.";

        return false;
    }

    producto.classList.remove("is-invalid");
    producto.classList.add("is-valid");

    return true;
}

function validarDescripcion() {

    if (descripcion.value.trim() === "") {

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        document.getElementById("errorDescripcion").textContent =
            "La descripción es obligatoria.";

        return false;
    }

    if (descripcion.value.trim().length < 10) {

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        document.getElementById("errorDescripcion").textContent =
            "Debe contener al menos 10 caracteres.";

        return false;
    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    return true;
}

function validarCategoria() {

    if (categoria.value === "") {

        categoria.classList.remove("is-valid");
        categoria.classList.add("is-invalid");

        document.getElementById("errorCategoria").textContent =
            "Seleccione una categoría.";

        return false;
    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    return true;
}

// ==========================
// EVENTOS EN TIEMPO REAL
// ==========================

cliente.addEventListener("input", validarCliente);
cliente.addEventListener("blur", validarCliente);

producto.addEventListener("input", validarProducto);
producto.addEventListener("blur", validarProducto);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);

// ==========================
// REGISTRAR PEDIDO
// ==========================

formulario.addEventListener("submit", function (event) {

    event.preventDefault();

    const formularioValido =
        validarCliente() &&
        validarProducto() &&
        validarDescripcion() &&
        validarCategoria();

    if (!formularioValido) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Corrija los errores antes de registrar el pedido.
            </div>
        `;

        return;
    }

    const pedido = {

        cliente: cliente.value,
        producto: producto.value,
        descripcion: descripcion.value,
        categoria: categoria.value

    };

    pedidos.push(pedido);

    mostrarPedidos();

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Pedido registrado correctamente.
        </div>
    `;

    formulario.reset();

    cliente.classList.remove("is-valid");
    producto.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

});

// ==========================
// MOSTRAR PEDIDOS
// ==========================

function mostrarPedidos() {

    listaPedidos.innerHTML = "";

    // Condición solicitada

    if (pedidos.length === 0) {

        listaPedidos.innerHTML = `
            <div class="alert alert-info">
                Aún no existen pedidos registrados.
            </div>
        `;

    } else {

        pedidos.forEach(function (pedido, indice) {

            listaPedidos.innerHTML += `

            <div class="card shadow mt-3">

                <div class="card-body">

                    <h5>${pedido.cliente}</h5>

                    <p><strong>Producto:</strong> ${pedido.producto}</p>

                    <p><strong>Descripción:</strong> ${pedido.descripcion}</p>

                    <p><strong>Categoría:</strong> ${pedido.categoria}</p>

                    <button
                        class="btn btn-danger btn-sm"
                        onclick="eliminarPedido(${indice})">

                        Eliminar

                    </button>

                </div>

            </div>

            `;

        });

    }

    contador.textContent = pedidos.length;

}

// ==========================
// ELIMINAR PEDIDO
// ==========================

function eliminarPedido(indice) {

    pedidos.splice(indice, 1);

    mostrarPedidos();

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Pedido eliminado correctamente.
        </div>
    `;

}

// Mostrar estado inicial
mostrarPedidos();
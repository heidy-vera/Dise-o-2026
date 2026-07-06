// Obtener elementos del formulario

const formulario = document.getElementById("formPedido");

const cliente = document.getElementById("cliente");
const producto = document.getElementById("producto");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const listaPedidos = document.getElementById("listaPedidos");
const contador = document.getElementById("contador");
const mensaje = document.getElementById("mensaje");

// Arreglo para almacenar los pedidos

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

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    let formularioValido =
        validarCliente() &&
        validarProducto() &&
        validarDescripcion() &&
        validarCategoria();

    if(!formularioValido){

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

function mostrarPedidos(){

    listaPedidos.innerHTML = "";

    pedidos.forEach(function(pedido, indice){

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

    contador.textContent = pedidos.length;

}

// ==========================
// ELIMINAR PEDIDO
// ==========================

function eliminarPedido(indice){

    pedidos.splice(indice,1);

    mostrarPedidos();

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Pedido eliminado correctamente.
        </div>
    `;

}
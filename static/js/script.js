// =====================================
// VARIABLES
// =====================================

const formulario = document.getElementById("formPedido");

const cliente = document.getElementById("cliente");
const producto = document.getElementById("producto");
const categoria = document.getElementById("categoria");
const descripcion = document.getElementById("descripcion");

const errorCliente = document.getElementById("errorCliente");
const errorProducto = document.getElementById("errorProducto");
const errorCategoria = document.getElementById("errorCategoria");
const errorDescripcion = document.getElementById("errorDescripcion");

const listaPedidos = document.getElementById("listaPedidos");
const contador = document.getElementById("contador");

const mensaje = document.getElementById("mensaje");
const spinner = document.getElementById("spinner");

const detallePedido = document.getElementById("detallePedido");


// =====================================
// ARRAY DE PEDIDOS
// =====================================

let pedidos = JSON.parse(localStorage.getItem("pedidos")) || [];


// =====================================
// CARGAR PEDIDOS
// =====================================

document.addEventListener("DOMContentLoaded", () => {

    if (listaPedidos && contador) {
        mostrarPedidos();
    }

});


// =====================================
// VALIDACIONES
// =====================================

function validarCampo(campo, error, mensajeError) {

    if (!campo || !error) {
        return false;
    }

    if (campo.value.trim() === "") {

        campo.classList.add("is-invalid");
        campo.classList.remove("is-valid");

        error.textContent = mensajeError;

        return false;

    } else {

        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");

        error.textContent = "";

        return true;
    }
}


function validarFormulario() {

    let valido = true;

    valido =
        validarCampo(
            cliente,
            errorCliente,
            "Ingrese el nombre del cliente"
        ) && valido;


    valido =
        validarCampo(
            producto,
            errorProducto,
            "Ingrese el producto"
        ) && valido;


    valido =
        validarCampo(
            descripcion,
            errorDescripcion,
            "Ingrese una descripción"
        ) && valido;


    if (categoria && errorCategoria) {

        if (categoria.value === "") {

            categoria.classList.add("is-invalid");
            categoria.classList.remove("is-valid");

            errorCategoria.textContent =
                "Seleccione una categoría";

            valido = false;

        } else {

            categoria.classList.remove("is-invalid");
            categoria.classList.add("is-valid");

            errorCategoria.textContent = "";
        }
    }

    return valido;
}


// =====================================
// REGISTRAR PEDIDO
// =====================================

if (formulario) {

    formulario.addEventListener("submit", function (e) {

        e.preventDefault();

        if (!validarFormulario()) {

            mostrarMensaje(
                "Complete correctamente todos los campos",
                "danger"
            );

            return;
        }


        // Mostrar spinner

        if (spinner) {
            spinner.classList.remove("d-none");
        }


        setTimeout(() => {

            const nuevoPedido = {

                id: Date.now(),

                cliente: cliente.value.trim(),

                producto: producto.value.trim(),

                categoria: categoria.value,

                descripcion: descripcion.value.trim()

            };


            pedidos.push(nuevoPedido);

            guardarPedidos();

            mostrarPedidos();

            formulario.reset();

            limpiarEstados();


            if (spinner) {
                spinner.classList.add("d-none");
            }


            mostrarMensaje(
                "Pedido registrado correctamente",
                "success"
            );

        }, 1500);

    });

}


// =====================================
// GUARDAR EN LOCALSTORAGE
// =====================================

function guardarPedidos() {

    localStorage.setItem(
        "pedidos",
        JSON.stringify(pedidos)
    );

}


// =====================================
// MOSTRAR PEDIDOS EN TABLA
// =====================================

function mostrarPedidos() {

    if (!listaPedidos || !contador) {
        return;
    }

    listaPedidos.innerHTML = "";


    pedidos.forEach((pedido) => {

        const fila = document.createElement("tr");


        fila.innerHTML = `

            <td>${pedido.cliente}</td>

            <td>${pedido.producto}</td>

            <td>${pedido.categoria}</td>

            <td>${pedido.descripcion}</td>

            <td>

                <button
                    class="btn btn-primary btn-sm me-1"
                    onclick="verPedido(${pedido.id})">

                    <i class="bi bi-eye"></i>

                </button>


                <button
                    class="btn btn-danger btn-sm"
                    onclick="eliminarPedido(${pedido.id})">

                    <i class="bi bi-trash"></i>

                </button>

            </td>

        `;


        listaPedidos.appendChild(fila);

    });


    contador.textContent = pedidos.length;

}


// =====================================
// ELIMINAR PEDIDO
// =====================================

function eliminarPedido(id) {

    pedidos = pedidos.filter(
        pedido => pedido.id !== id
    );


    guardarPedidos();

    mostrarPedidos();


    mostrarMensaje(
        "Pedido eliminado correctamente",
        "warning"
    );

}


// =====================================
// MODAL DETALLE DEL PEDIDO
// =====================================

function verPedido(id) {

    const pedido = pedidos.find(
        p => p.id === id
    );


    if (!pedido || !detallePedido) {
        return;
    }


    detallePedido.innerHTML = `

        <strong>Cliente:</strong>
        ${pedido.cliente}

        <br><br>

        <strong>Producto:</strong>
        ${pedido.producto}

        <br><br>

        <strong>Categoría:</strong>
        ${pedido.categoria}

        <br><br>

        <strong>Descripción:</strong>
        ${pedido.descripcion}

    `;


    const modalElemento =
        document.getElementById("modalPedido");


    if (modalElemento) {

        const modal =
            new bootstrap.Modal(modalElemento);

        modal.show();

    }

}


// =====================================
// MENSAJES BOOTSTRAP
// =====================================

function mostrarMensaje(texto, tipo) {

    if (!mensaje) {
        return;
    }


    mensaje.className =
        `alert alert-${tipo} mt-3`;


    mensaje.textContent = texto;


    mensaje.classList.remove("d-none");


    setTimeout(() => {

        mensaje.classList.add("d-none");

    }, 3000);

}


// =====================================
// LIMPIAR ESTILOS DE VALIDACIÓN
// =====================================

function limpiarEstados() {

    const campos = [

        cliente,

        producto,

        categoria,

        descripcion

    ];


    campos.forEach(campo => {

        if (campo) {

            campo.classList.remove(
                "is-valid",
                "is-invalid"
            );

        }

    });

}
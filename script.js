document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("formPedido");
    const cliente = document.getElementById("cliente");
    const producto = document.getElementById("producto");
    const categoria = document.getElementById("categoria");

    const lista = document.getElementById("listaPedidos");
    const contador = document.getElementById("contador");
    const mensaje = document.getElementById("mensaje");

    let pedidos = JSON.parse(localStorage.getItem("pedidos")) || [];

    // ---------------------------
    // GUARDAR EN LOCALSTORAGE
    // ---------------------------
    const guardar = () => {
        localStorage.setItem("pedidos", JSON.stringify(pedidos));
    };

    // ---------------------------
    // MOSTRAR PEDIDOS
    // ---------------------------
    const mostrar = () => {
        lista.innerHTML = "";
        contador.textContent = pedidos.length;

        pedidos.forEach((p, i) => {
            const div = document.createElement("div");
            div.className = "alert alert-secondary mt-2";

            div.innerHTML = `
                <strong>${p.cliente}</strong> - 
                ${p.producto} (${p.categoria})
                <button class="btn btn-sm btn-danger float-end">Eliminar</button>
            `;

            div.querySelector("button").addEventListener("click", () => {
                pedidos.splice(i, 1);
                guardar();
                mostrar();
            });

            lista.appendChild(div);
        });
    };

    // ---------------------------
    // VALIDACIONES
    // ---------------------------
    const validarTexto = (input, min) => {
        if (input.value.trim().length >= min) {
            input.classList.add("is-valid");
            input.classList.remove("is-invalid");
            return true;
        } else {
            input.classList.add("is-invalid");
            input.classList.remove("is-valid");
            return false;
        }
    };

    const validarSelect = (select) => {
        if (select.value !== "") {
            select.classList.add("is-valid");
            select.classList.remove("is-invalid");
            return true;
        } else {
            select.classList.add("is-invalid");
            select.classList.remove("is-valid");
            return false;
        }
    };

    // ---------------------------
    // VALIDACIÓN EN TIEMPO REAL
    // ---------------------------
    cliente.addEventListener("input", () => validarTexto(cliente, 3));
    producto.addEventListener("input", () => validarTexto(producto, 2));
    categoria.addEventListener("change", () => validarSelect(categoria));

    // ---------------------------
    // SUBMIT
    // ---------------------------
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const v1 = validarTexto(cliente, 3);
        const v2 = validarTexto(producto, 2);
        const v3 = validarSelect(categoria);

        if (!v1 || !v2 || !v3) {
            mensaje.innerHTML = `
                <div class="alert alert-danger">
                     Por favor complete todos los campos correctamente
                </div>
            `;
            return;
        }

        const nuevo = {
            cliente: cliente.value.trim(),
            producto: producto.value.trim(),
            categoria: categoria.value
        };

        pedidos.push(nuevo);
        guardar();

        form.reset();

        cliente.classList.remove("is-valid");
        producto.classList.remove("is-valid");
        categoria.classList.remove("is-valid");

        mensaje.innerHTML = `
            <div class="alert alert-success">
                 Pedido registrado correctamente
            </div>
        `;

        mostrar();
    });

    // Inicializar
    mostrar();
});

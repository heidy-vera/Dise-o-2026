
// Obtener los elementos del HTML
const formulario = document.getElementById("formPedido");
const lista = document.getElementById("listaPedidos");
const mensaje = document.getElementById("mensaje");
const contador = document.getElementById("contador");

// Variable para contar los pedidos
let total = 0;

// Evento al enviar el formulario
formulario.addEventListener("submit", function(event){

    // Evita que la página se recargue
    event.preventDefault();

    // Obtener los datos del formulario
    const cliente = document.getElementById("cliente").value.trim();
    const producto = document.getElementById("producto").value.trim();
    const categoria = document.getElementById("categoria").value;

    // Validación
    if(cliente === "" || producto === "" || categoria === ""){

        mensaje.innerHTML =
        "<div class='alert alert-danger'>Complete todos los campos.</div>";

        return;
    }

    // Mensaje de éxito
    mensaje.innerHTML =
    "<div class='alert alert-success'>Pedido registrado correctamente.</div>";

    // Crear la tarjeta
    const tarjeta = document.createElement("div");
    tarjeta.className = "card shadow p-3 mb-3";

    // Crear el contenido
    const texto = document.createElement("p");

    texto.innerHTML =
    "<strong>Cliente:</strong> " + cliente +
    "<br><strong>Producto:</strong> " + producto +
    "<br><strong>Categoría:</strong> " + categoria;

    // Crear botón eliminar
    const boton = document.createElement("button");

    boton.textContent = "Eliminar";

    boton.className = "btn btn-danger";

    // Evento para eliminar
    boton.addEventListener("click", function(){

        lista.removeChild(tarjeta);

        total--;

        contador.textContent = total;

    });

    // Agregar elementos a la tarjeta
    tarjeta.appendChild(texto);
    tarjeta.appendChild(boton);

    // Mostrar la tarjeta en la página
    lista.appendChild(tarjeta);

    // Actualizar contador
    total++;

    contador.textContent = total;

    // Limpiar formulario
    formulario.reset();

});

document.addEventListener("DOMContentLoaded", function () {
    console.log("📦 sc.js cargado");

    if (typeof idCarrito === "undefined" || !idCarrito || isNaN(idCarrito)) {
        console.error("❌ idCarrito inválido:", idCarrito);
        return;
    }

    if (typeof BASE_API === 'undefined') {
        alert("❌ BASE_API no está definido.");
        return;
    }

    const container = document.querySelector(".container");
    const resumenPrecio = document.querySelector(".resumen-compra .card-text");

    if (!container) {
        console.error("❌ No se encontró el contenedor .container en el DOM.");
        return;
    }

    console.log("🧠 BASE_API:", BASE_API);
    console.log("🛒 idCarrito:", idCarrito);
    console.log(`📤 GET: ${BASE_API}/carrito/${idCarrito}`);

    fetch(`${BASE_API}/carrito/${idCarrito}`)
        .then(res => res.json())
        .then(data => {
            console.log("📥 Datos recibidos:", data);

            if (data.error) {
                console.error("❌ Error desde API:", data.error);
                container.innerHTML += `<p style="color: red;">${data.error}</p>`;
                return;
            }

            let html = `<ul style="list-style: none; padding: 0;">`;

            data.productos.forEach(item => {
                html += `
                    <li style="margin-bottom: 10px;">
                        <strong>${item.nombre_producto}</strong><br>
                        <span style="font-size: 0.9em; color: gray;">Local: ${item.nombre_local}</span><br>
                        ${item.cantidad} unidad(es) x $${item.precio_unitario} = 
                        $${item.subtotal}
                    </li>
                `;
            });

            html += `</ul><hr><p><strong>Total:</strong> $${data.total_carrito}</p>`;

            container.innerHTML = `
                <h2 style="color:rgb(0, 0, 0); margin: 30px;">Carrito de Compras</h2>
                ${html}
            `;

            if (resumenPrecio) {
                resumenPrecio.textContent = "Precio: $" + data.total_carrito;
            }
        })
        .catch(err => {
            console.error("❌ Error al obtener el carrito:", err);
            container.innerHTML += `<p style="color: red;">Error al cargar el carrito.</p>`;
        });
});
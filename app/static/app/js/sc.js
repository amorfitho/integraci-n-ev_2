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
    const direccionInput = document.getElementById("direccion-input");
    const guardarDireccionBtn = document.getElementById("guardar-direccion");
    const pagoBtn = document.getElementById("pago-btn");

    function validarDireccion(valor) {
        return valor.trim() !== "" && valor.trim() !== "-";
    }

    function actualizarBotonPago(direccion) {
        if (validarDireccion(direccion)) {
            pagoBtn.classList.remove("disabled");
            pagoBtn.style.pointerEvents = "auto";
        } else {
            pagoBtn.classList.add("disabled");
            pagoBtn.style.pointerEvents = "none";
        }
    }

    console.log("🧠 BASE_API:", BASE_API);
    console.log("🛒 idCarrito:", idCarrito);

    // Cargar datos del carrito
    fetch(`${BASE_API}/carrito/${idCarrito}`)
        .then(res => res.json())
        .then(data => {
            console.log("📥 Datos recibidos:", data);

            if (data.error) {
                console.error("❌ Error desde API:", data.error);
                container.innerHTML += `<p style="color: red;">${data.error}</p>`;
                return;
            }

            // Dirección: cargar valor y estado del botón
            if (direccionInput && guardarDireccionBtn && pagoBtn) {
                direccionInput.value = data.direccion_cliente || "";
                actualizarBotonPago(direccionInput.value);

                guardarDireccionBtn.addEventListener("click", () => {
                    const nuevaDireccion = direccionInput.value.trim();
                    if (!validarDireccion(nuevaDireccion)) {
                        alert("❌ Dirección inválida. Ingrese una dirección válida.");
                        return;
                    }

                    fetch(`${BASE_API}/carrito/${idCarrito}/cambiar_direccion`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ direccion_cliente: nuevaDireccion })
                    })
                    .then(res => res.json())
                    .then(resp => {
                        if (resp.error) {
                            alert("❌ " + resp.error);
                        } else {
                            alert("✅ Dirección actualizada correctamente.");
                            actualizarBotonPago(nuevaDireccion);
                        }
                    })
                    .catch(err => {
                        console.error("❌ Error al actualizar dirección:", err);
                        alert("❌ Error al actualizar la dirección");
                    });
                });
            }

            // Renderizar productos
            let html = `<ul style="list-style: none; padding: 0;">`;
            data.productos.forEach(item => {
                html += `
                    <li style="margin-bottom: 10px;">
                        <strong>${item.nombre_producto}</strong><br>
                        <span style="font-size: 0.9em; color: gray;">Local: ${item.nombre_local}</span><br>
                        ${item.cantidad} unidad(es) x $${item.precio_unitario} = $${item.subtotal}<br>
                        <button class="quitar-uno" 
                                data-producto-id="${item.producto_id}" 
                                data-local-id="${item.id_local}">➖</button>
                        <button class="agregar-uno" 
                                data-producto-id="${item.producto_id}" 
                                data-local-id="${item.id_local}">➕</button>
                        <button class="eliminar-producto" 
                                data-producto-id="${item.producto_id}" 
                                data-local-id="${item.id_local}">🗑️</button>
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

            // ➖ Quitar 1 unidad
            document.querySelectorAll(".quitar-uno").forEach(btn => {
                btn.addEventListener("click", () => {
                    const productoId = parseInt(btn.dataset.productoId);
                    const localId = parseInt(btn.dataset.localId);

                    fetch(`${BASE_API}/carrito/${idCarrito}/quitar_producto`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            producto_id: productoId,
                            local_id: localId,
                            cantidad: 1
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) {
                            alert("❌ " + data.error);
                        } else {
                            console.log("➖", data.message);
                            location.reload();
                        }
                    });
                });
            });

            // ➕ Agregar 1 unidad
            document.querySelectorAll(".agregar-uno").forEach(btn => {
                btn.addEventListener("click", () => {
                    const productoId = parseInt(btn.dataset.productoId);
                    const localId = parseInt(btn.dataset.localId);

                    fetch(`${BASE_API}/carrito/${idCarrito}/agregar_producto`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            producto_id: productoId,
                            local_id: localId,
                            cantidad: 1
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) {
                            alert("❌ " + data.error);
                        } else {
                            console.log("➕", data.message);
                            location.reload();
                        }
                    });
                });
            });

            // 🗑️ Eliminar completamente
            document.querySelectorAll(".eliminar-producto").forEach(btn => {
                btn.addEventListener("click", () => {
                    const productoId = parseInt(btn.dataset.productoId);
                    const localId = parseInt(btn.dataset.localId);

                    fetch(`${BASE_API}/carrito/${idCarrito}/quitar_producto`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            producto_id: productoId,
                            local_id: localId,
                            cantidad: 99999
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) {
                            alert("❌ " + data.error);
                        } else {
                            console.log("🗑️", data.message);
                            location.reload();
                        }
                    });
                });
            });
        })
        .catch(err => {
            console.error("❌ Error al obtener el carrito:", err);
            container.innerHTML += `<p style="color: red;">Error al cargar el carrito.</p>`;
        });
});

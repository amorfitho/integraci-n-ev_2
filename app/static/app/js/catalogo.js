document.addEventListener("DOMContentLoaded", function () {
    if (typeof BASE_API === 'undefined') {
        alert("❌ BASE_API no está definido. Asegúrate de que el HTML lo defina antes de cargar este script.");
        return;
    }

    const botonesAgregar = document.querySelectorAll(".add-to-cart");

    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", function () {
            const productoId = parseInt(this.dataset.productId);
            const localId = parseInt(this.dataset.localId);
            const idCarrito = parseInt(this.dataset.idCarrito);
            const cantidad = 1;

            if (!productoId || !localId || !idCarrito) {
                alert("❌ Datos inválidos. Revisa los atributos del botón.");
                return;
            }

            const textoOriginal = this.textContent;
            this.disabled = true;
            this.textContent = "Agregando...";

            console.log("➡️ Enviando a:", `${BASE_API}/carrito/${idCarrito}/agregar_producto`);
            console.log("➡️ Datos:", { productoId, localId, cantidad });

            fetch(`${BASE_API}/carrito/${idCarrito}/agregar_producto`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    producto_id: productoId,
                    local_id: localId,
                    cantidad: cantidad
                })
            })
            .then(async response => {
                const data = await response.json().catch(() => null);
                if (!response.ok) {
                    throw new Error(data?.error || 'Error desconocido');
                }
                alert("✅ " + data.message);
            })
            .catch(error => {
                alert("❌ Error: " + error.message);
                console.error(error);
            })
            .finally(() => {
                setTimeout(() => {
                    boton.disabled = false;
                    boton.textContent = textoOriginal;
                }, 1000);
            });
        });
    });
});

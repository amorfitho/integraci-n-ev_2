const BASE_API = "http://192.168.4.31:5000"; // ✅ IP correcta

document.addEventListener("DOMContentLoaded", function () {
    const botonesAgregar = document.querySelectorAll(".add-to-cart");

    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", function () {
            const productoId = this.dataset.productId;
            const localId = this.dataset.localId;
            const idCarrito = this.dataset.idCarrito;
            const cantidad = 1;

            const textoOriginal = this.textContent;
            this.disabled = true;
            this.textContent = "Agregando...";

            console.log("Enviando a Flask:", {
                producto_id: productoId,
                local_id: localId,
                cantidad: cantidad
            });

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
                alert("❌ " + error.message);
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

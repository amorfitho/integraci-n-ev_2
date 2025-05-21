import sqlite3
import os

db_path = os.path.abspath("db.sqlite3")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS app_carrito (
    id_carrito INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_rut TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL,
    estado TEXT NOT NULL CHECK (estado IN ('abierto', 'pagado', 'cerrado')),
    FOREIGN KEY (usuario_rut) REFERENCES app_usuario(rut)
);

CREATE TABLE IF NOT EXISTS app_carrito_item (
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    carrito_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario INTEGER NOT NULL,
    FOREIGN KEY (carrito_id) REFERENCES app_carrito(id_carrito),
    FOREIGN KEY (producto_id) REFERENCES app_producto(id_producto)
);
""")

conn.commit()
conn.close()

print("✅ Tablas de carrito creadas con éxito.")
import sqlite3
import os

# Ruta absoluta a la base de datos
db_path = os.path.abspath("db.sqlite3")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Renombrar la tabla original
    cursor.execute("ALTER TABLE app_producto RENAME TO app_producto_old;")

    # Crear nueva tabla con las columnas modificadas
    cursor.execute("""
        CREATE TABLE app_producto (
            id_producto INTEGER PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            precio_minorista INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            familia_id INTEGER NOT NULL,
            fecha_fabricacion DATE,
            imagen VARCHAR(100),
            stock_minimo INTEGER DEFAULT 5,
            precio_mayorista INTEGER DEFAULT 0
        );
    """)

    # Copiar los datos de la tabla antigua a la nueva
    cursor.execute("""
        INSERT INTO app_producto (
            id_producto, nombre, precio_minorista, descripcion, familia_id,
            fecha_fabricacion, imagen, stock_minimo
        )
        SELECT id_producto, nombre, precio, descripcion, familia_id,
               fecha_fabricacion, imagen, stock_minimo
        FROM app_producto_old;
    """)

    # Calcular y actualizar el precio mayorista (80% del precio minorista)
    cursor.execute("""
        UPDATE app_producto
        SET precio_mayorista = ROUND(precio_minorista * 0.8);
    """)

    # Eliminar la tabla antigua
    cursor.execute("DROP TABLE app_producto_old;")

    conn.commit()
    print("✔️ Columnas modificadas correctamente.")

except Exception as e:
    print("❌ Error:", e)

finally:
    conn.close()

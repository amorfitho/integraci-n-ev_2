import sqlite3
import os

# Ruta dinámica hacia la base de datos db.sqlite3
db_path = os.path.abspath("db.sqlite3")

def agregar_columna_direccion_cliente():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Verificar si la tabla app_carrito existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_carrito'")
        if not cursor.fetchone():
            print("❌ La tabla 'app_carrito' no existe en la base de datos.")
            return

        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(app_carrito)")
        columnas = [col[1] for col in cursor.fetchall()]
        if 'direccion_cliente' in columnas:
            print("✅ La columna 'direccion_cliente' ya existe en 'app_carrito'. No se realizó ningún cambio.")
            return

        # Agregar la columna con valor por defecto '-'
        cursor.execute("ALTER TABLE app_carrito ADD COLUMN direccion_cliente TEXT DEFAULT '-'")
        conn.commit()
        print("✅ Columna 'direccion_cliente' agregada exitosamente a 'app_carrito' con valor por defecto '-'.")

    except Exception as e:
        print("❌ Error al modificar la tabla:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    agregar_columna_direccion_cliente()

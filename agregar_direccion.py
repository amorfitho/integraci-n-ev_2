import sqlite3
import os

# Ruta dinámica hacia la base de datos db.sqlite3
db_path = os.path.abspath("db.sqlite3")

def agregar_columna_direccion():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(app_usuario)")
        columnas = [col[1] for col in cursor.fetchall()]
        if 'direccion' in columnas:
            print("✅ La columna 'direccion' ya existe en 'app_usuario'. No se realizó ningún cambio.")
            return

        # Agregar la columna con valor por defecto '-'
        cursor.execute("ALTER TABLE app_usuario ADD COLUMN direccion TEXT DEFAULT '-'")
        conn.commit()
        print("✅ Columna 'direccion' agregada exitosamente a 'app_usuario' con valor por defecto '-'.")

    except Exception as e:
        print("❌ Error al modificar la tabla:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    agregar_columna_direccion()
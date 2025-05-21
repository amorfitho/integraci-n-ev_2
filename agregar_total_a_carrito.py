import sqlite3
import os

# Ruta a la base de datos
db_path = os.path.abspath("db.sqlite3")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE app_carrito ADD COLUMN total_carrito INTEGER DEFAULT 0
    """)
    print("✅ Columna 'total_carrito' agregada con éxito.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("⚠️ La columna 'total_carrito' ya existe.")
    else:
        print("❌ Error al agregar la columna:", e)
finally:
    conn.commit()
    conn.close()

import sqlite3
import os

db_path = os.path.abspath("db.sqlite3")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Intentar agregar la columna (solo si no existe)
    cursor.execute("""
        ALTER TABLE app_carrito 
        ADD COLUMN tipo_cliente TEXT CHECK (tipo_cliente IN ('b2b', 'b2c')) DEFAULT 'b2c'
    """)
    print("✅ Columna 'tipo_cliente' agregada con éxito.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("⚠️ La columna 'tipo_cliente' ya existe.")
    else:
        print("❌ Error al alterar la tabla:", e)
finally:
    conn.commit()
    conn.close()

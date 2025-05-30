import sqlite3
import os

# Ajusta el nombre si tu archivo tiene otro nombre
db_path = os.path.abspath("db.sqlite3")

# Conexión a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar si la columna ya existe
cursor.execute("PRAGMA table_info(app_carrito_item)")
columnas = [col[1] for col in cursor.fetchall()]
if 'local_id' not in columnas:
    # Agregar la columna local_id
    cursor.execute("""
        ALTER TABLE app_carrito_item
        ADD COLUMN local_id INTEGER REFERENCES app_local(id_local)
    """)
    print("Columna 'local_id' agregada exitosamente.")
else:
    print("La columna 'local_id' ya existe.")

conn.commit()
conn.close()
import sqlite3
import os

# Ajusta el nombre si tu archivo tiene otro nombre
db_path = os.path.abspath("db.sqlite3")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE app_producto ADD COLUMN stock_minimo INTEGER DEFAULT 5;")
    conn.commit()
    print("Columna 'stock_minimo' agregada correctamente.")
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
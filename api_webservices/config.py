from app import app
from flaskext.mysql import MySQL
import sqlite3
import os

# def get_db_connection():
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # sube una carpeta
#     db_path = os.path.join(base_dir, 'db.sqlite3')  # ajusta al nombre exacto del archivo
#     conn = sqlite3.connect(db_path)
#     conn.row_factory = sqlite3.Row
#     return conn

# Ruta fija
db_path = r"C:\Users\felip\Desktop\integraci-n-ev_2\db.sqlite3"

print("✅ CONFIG.PY cargado correctamente")
print("→ db_path apuntando a:", db_path)

def get_db_connection():
    print("✅ FLASK ESTÁ USANDO ESTA DB:", db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
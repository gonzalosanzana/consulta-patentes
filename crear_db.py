import sqlite3

# Conectar o crear la base de datos
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS patentes (
    patente TEXT PRIMARY KEY,
    nombre TEXT,
    apellido TEXT
)
""")

# Insertar algunos datos de ejemplo
datos = [
    ("SKBK-93", "Juan", "Pérez"),
    ("ABCD-12", "María", "López"),
    ("ZXCV-45", "Pedro", "Gómez")
]

cursor.executemany("INSERT OR REPLACE INTO patentes VALUES (?, ?, ?)", datos)

conn.commit()
conn.close()


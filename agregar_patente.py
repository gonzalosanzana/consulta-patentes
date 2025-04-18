import sqlite3

# Datos a agregar (puedes modificar esta lista)
datos = [
    ("QQQQ-11", "Lucía", "Martínez"),
    ("PPPP-22", "Carlos", "Sánchez"),
    ("YYYY-33", "Ana", "Ramírez")
]

# Conectarse a la base de datos
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Insertar los datos
for patente, nombre, apellido in datos:
    cursor.execute("INSERT INTO patentes (patente, nombre, apellido) VALUES (?, ?, ?)", (patente, nombre, apellido))

conn.commit()
conn.close()

print("✅ Patentes agregadas con éxito")

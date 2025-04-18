import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Consultar todas las filas de la tabla
cursor.execute("SELECT * FROM patentes")
filas = cursor.fetchall()

# Mostrar los resultados
for fila in filas:
    print(f"Patente: {fila[0]} - Nombre: {fila[1]} - Apellido: {fila[2]}")

conn.close()


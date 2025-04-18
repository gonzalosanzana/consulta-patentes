from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Permitir conexión desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/buscar")
def buscar_patente(patente: str):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellido FROM patentes WHERE patente = ?", (patente.upper(),))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return {"nombre": resultado[0], "apellido": resultado[1]}
    else:
        return {"error": "Patente no encontrada"}



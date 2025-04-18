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

from fastapi.responses import JSONResponse

@app.get("/")
def root():
    return JSONResponse(content={"mensaje": "Bienvenido. Usa /buscar?patente=XXXX-YY para consultar."})

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Form

@app.get("/formulario", response_class=HTMLResponse)
def formulario():
    return """
    <html>
        <head>
            <title>Consulta de Patentes</title>
            <style>
                body { font-family: Arial; background: #f9f9f9; text-align: center; padding: 40px; }
                input, button { padding: 10px; margin-top: 10px; width: 200px; }
                .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); display: inline-block; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>🔍 Consulta de Patentes</h2>
                <form action="/consultar" method="post">
                    <input type="text" name="patente" placeholder="Ej: SKBK-93" required /><br />
                    <button type="submit">Consultar</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/consultar", response_class=HTMLResponse)
async def consultar(patente: str = Form(...)):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellido FROM patentes WHERE patente = ?", (patente,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre, apellido = resultado
        respuesta = f"<p>✅ Dueño: <strong>{nombre} {apellido}</strong></p>"
    else:
        respuesta = "<p>❌ Patente no encontrada</p>"

    return f"""
    <html>
        <head>
            <title>Resultado</title>
            <style>
                body {{ font-family: Arial; background: #f9f9f9; text-align: center; padding: 40px; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); display: inline-block; }}
                a {{ display: block; margin-top: 20px; text-decoration: none; color: #007bff; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Resultado de la búsqueda</h2>
                {respuesta}
                <a href="/formulario">🔙 Volver</a>
            </div>
        </body>
    </html>
    """


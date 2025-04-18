from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

# Ruta principal redirige al formulario
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <script>window.location.href='/formulario';</script>
    """

# Página del formulario con diseño
@app.get("/formulario", response_class=HTMLResponse)
def formulario():
    return """
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Consulta de Patentes</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f0f2f5;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                header {
                    background-color: #007bff;
                    width: 100%;
                    padding: 20px 0;
                    color: white;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                }
                .card {
                    background: white;
                    margin-top: 40px;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    width: 90%;
                    max-width: 400px;
                    text-align: center;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    margin-top: 10px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    font-size: 16px;
                }
                button {
                    margin-top: 20px;
                    padding: 12px;
                    background-color: #007bff;
                    border: none;
                    color: white;
                    width: 100%;
                    font-size: 16px;
                    border-radius: 8px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
                footer {
                    margin-top: 40px;
                    font-size: 14px;
                    color: #666;
                    text-align: center;
                    padding-bottom: 30px;
                }
                .ad-placeholder {
                    background-color: #e9ecef;
                    border: 1px dashed #adb5bd;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 10px;
                    color: #495057;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <header>🔍 Consulta de Patentes Chilenas</header>
            
            <!-- 🟡 Espacio para publicidad -->
            <div class="ad-placeholder">[Publicidad aquí]</div>
            
            <div class="card">
                <form action="/consultar" method="post">
                    <label for="patente">Ingresa la patente:</label><br>
                    <input type="text" name="patente" placeholder="Ej: SKBK-93" required />
                    <button type="submit">Consultar</button>
                </form>
            </div>

            <!-- 🟡 Otro espacio para publicidad -->
            <div class="ad-placeholder">[Publicidad aquí]</div>

            <footer>
                Consulta 100% gratuita - Datos referenciales<br>
                © 2025 Consulta Patentes
            </footer>
        </body>
    </html>
    """

# Ruta que procesa el formulario
@app.post("/consultar", response_class=HTMLResponse)
async def consultar(patente: str = Form(...)):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellido FROM patentes WHERE patente = ?", (patente,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nombre, apellido = resultado
        mensaje = f"<p>✅ Dueño encontrado:</p><h3>{nombre} {apellido}</h3>"
    else:
        mensaje = "<p>❌ No se encontró dueño para esta patente.</p>"

    return f"""
    <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resultado</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: #f0f2f5;
                    text-align: center;
                    padding: 40px;
                }}
                .card {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    display: inline-block;
                    width: 90%;
                    max-width: 400px;
                }}
                a {{
                    margin-top: 20px;
                    display: inline-block;
                    text-decoration: none;
                    color: #007bff;
                }}
                .ad-placeholder {{
                    background-color: #e9ecef;
                    border: 1px dashed #adb5bd;
                    padding: 20px;
                    margin: 30px auto;
                    border-radius: 10px;
                    color: #495057;
                    font-size: 14px;
                    max-width: 400px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Resultado</h2>
                {mensaje}
                <a href="/formulario">🔙 Volver al formulario</a>
            </div>
            <div class="ad-placeholder">[Publicidad aquí]</div>
        </body>
    </html>
    """

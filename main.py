from flask import Flask, render_template, request
from scraper import obtener_resultados
from datetime import datetime
import json
import os

app = Flask(__name__)

@app.route('/resumen')
def resumen():
    try:
        with open("historial.json", "r", encoding="utf-8") as f:
            registros = [json.loads(line) for line in f.readlines()]
    except:
        registros = []

    if registros:
        ultimo = registros[-1]
        return render_template("resumen.html", registro=ultimo)
    else:
        return "Sin datos disponibles", 200

@app.route('/')
def index():
    registros = []

    # Cargar todos los registros desde historial.json
    try:
        with open("historial.json", "r", encoding="utf-8") as f:
            registros = [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        registros = []

    # Buscar por fecha si el usuario seleccionó una
    fecha_input = request.args.get('fecha')
    if fecha_input:
        try:
            fecha_filtrada = datetime.strptime(fecha_input, "%Y-%m-%d").strftime("%d/%m/%Y")
            registros = [r for r in registros if r["fecha"].startswith(fecha_filtrada)]
        except:
            pass

    return render_template("resultados.html", registros=registros, fecha=fecha_input)

@app.route('/actualizar')
def actualizar():
    try:
        obtener_resultados()
        return "✅ Actualización completada", 200
    except Exception as e:
        return f"❌ Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

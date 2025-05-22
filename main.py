from flask import Flask, render_template
from scraper import obtener_resultados, guardar_historial
import os

app = Flask(__name__)

@app.route('/')
def home():
    loterias, timestamp = obtener_resultados()
    guardar_historial(loterias, timestamp)
    return render_template("resultados.html", loterias=loterias, actualizacion=timestamp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

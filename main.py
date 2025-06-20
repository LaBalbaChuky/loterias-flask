from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, render_template
from scraper import obtener_resultados, agrupar_loterias
import os  # ⬅️ NECESARIO

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    loterias, actualizacion = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    return render_template("resultados.html", grupos=grupos, actualizacion=actualizacion)
    


@app.route('/api')
def api():
    loterias, timestamp = obtener_resultados()
    return jsonify({
        "actualizacion": timestamp,
        "loterias": loterias
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


app = Flask(__name__)
CORS(app)  # permite acceso desde tu frontend

@app.route('/api')
def api():
    loterias, timestamp = obtener_resultados()
    return jsonify({
        "actualizacion": timestamp,
        "loterias": loterias
    })


@app.route('/actualizar')
def actualizar():
    loterias, timestamp = obtener_resultados()
    guardar_historial(loterias, timestamp)
    return f"✅ Datos actualizados: {timestamp}", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

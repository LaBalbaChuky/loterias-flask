from flask import Flask, jsonify
from flask_cors import CORS
from scraper import obtener_resultados

app = Flask(__name__)
CORS(app)  # permite acceso desde tu frontend

@app.route('/api')
def api():
    loterias, timestamp = obtener_resultados()
    return jsonify({
        "actualizacion": timestamp,
        "loterias": loterias
    })

@app.route('/')
def home():
    loterias, timestamp = obtener_resultados()
    guardar_historial(loterias, timestamp)
    return render_template("resultados.html", loterias=loterias, actualizacion=timestamp)

@app.route('/actualizar')
def actualizar():
    loterias, timestamp = obtener_resultados()
    guardar_historial(loterias, timestamp)
    return f"✅ Datos actualizados: {timestamp}", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

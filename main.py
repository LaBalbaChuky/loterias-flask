from flask import Flask, jsonify
from flask_cors import CORS
from flask import Flask, render_template
from scraper import obtener_resultados, agrupar_loterias, crear_html, guardar_html
from upload_to_netlify import subir_a_netlify
import os  # ⬅️ NECESARIO




from scraper import (
    obtener_resultados,
    agrupar_loterias,
    crear_html,
    guardar_html
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    loterias, actualizacion = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    html = crear_html(grupos, actualizacion)
    guardar_html(html)  # 👈 Genera el index.html automáticamente
    return render_template("resultados.html", grupos=grupos, actualizacion=actualizacion)

@app.route("/api")
def api():
    loterias, timestamp = obtener_resultados()
    return jsonify({
        "actualizacion": timestamp,
        "loterias": loterias
    })

@app.route("/actualizar")
def actualizar():
    loterias, timestamp = obtener_resultados()
    html = crear_html(agrupar_loterias(loterias), timestamp)
    guardar_html(html)
    return f"✅ Datos actualizados: {timestamp}", 200



if __name__ == "__main__":
    loterias, timestamp = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    html = crear_html(grupos, timestamp)
    guardar_html(html)
    print("✅ HTML generado correctamente en public/index.html")

    # Guardar el HTML generado
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Subir a Netlify automáticamente
    subir_a_netlify()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

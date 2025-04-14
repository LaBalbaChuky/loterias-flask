from flask import Flask
import scraper
import subir

app = Flask(__name__)

@app.route('/')
def ejecutar():
    try:
        scraper.main()
        subir.main()
        return "✅ Resultados actualizados y subidos a PythonAnywhere", 200
    except Exception as e:
        return f"❌ Error al actualizar: {e}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

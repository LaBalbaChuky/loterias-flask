import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def obtener_resultados():
    url = "https://loteriasdominicanas.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    loterias = []

    for item in soup.find_all("div", class_="game-block"):
        nombre = item.find("a", class_="game-title")
        fecha = item.find("div", class_="session-date")
        numeros = [n.text.strip() for n in item.find_all("span", class_="score")]
        img = item.find("img", class_="lazy")

        loterias.append({
            "nombre": nombre.text.strip() if nombre else "Desconocido",
            "fecha": fecha.text.strip() if fecha else "No disponible",
            "numeros": numeros,
            "imagen": f"https://loteriasdominicanas.com{img.get('data-src')}" if img and img.get("data-src") else "https://via.placeholder.com/100"
        })

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return loterias, timestamp

def crear_html(loterias, timestamp):
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Resultados de Hoy RD</title>
  <style>
    body {{ font-family: 'Segoe UI', sans-serif; background: #f4f6f8; margin: 0; padding: 0; }}
    header {{ background: linear-gradient(to right, #004aad, #0066cc); text-align: center; padding: 20px; }}
    header img {{ width: 250px; }}
    .actualizacion {{ text-align: center; margin: 15px; color: #555; }}
    .contenedor {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; padding: 20px; }}
    .tarjeta {{ background: #fff; border-radius: 10px; width: 260px; box-shadow: 0 3px 8px rgba(0,0,0,0.1); padding: 15px; text-align: center; }}
    .tarjeta img {{ height: 50px; margin-bottom: 10px; }}
    .tarjeta h3 {{ margin: 5px 0; color: #004aad; }}
    .numeros {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 10px; }}
    .bola {{ background: #fbc02d; border-radius: 50%; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; font-weight: bold; }}
    footer {{ background: #003366; color: white; text-align: center; padding: 12px; margin-top: 20px; }}
  </style>
</head>
<body>
  <header>
    <img src="https://cdn-lottery.kiskoo.com/63e850adcd8910c986e861e8fbab7d34.png" alt="Resultados de Hoy RD">
  </header>

  <div class="actualizacion">Última actualización: {timestamp}</div>

  <div class="contenedor">
    {''.join(f"""
      <div class="tarjeta">
        <img src="{l['imagen']}" alt="{l['nombre']}">
        <h3>{l['nombre']}</h3>
        <p>{l['fecha']}</p>
        <div class="numeros">{''.join(f'<div class="bola">{n}</div>' for n in l['numeros'])}</div>
      </div>
    """ for l in loterias)}
  </div>

  <footer>
    © {datetime.now().year} Resultados de Hoy RD. Todos los derechos reservados.
  </footer>
</body>
</html>
"""
    return html

def guardar_html(html):
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML generado correctamente en public/index.html")

if __name__ == "__main__":
    loterias, ts = obtener_resultados()
    html = crear_html(loterias, ts)
    guardar_html(html)

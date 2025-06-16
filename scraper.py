from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

def obtener_resultados():
    url = "https://loteriasdominicanas.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    loterias = []

    for item in soup.find_all('div', class_='game-block'):
        loteria = {}

        nombre_tag = item.find('a', class_='game-title')
        loteria['nombre'] = nombre_tag.text.strip() if nombre_tag else "Nombre no disponible"

        fecha_tag = item.find('div', class_='session-date')
        loteria['fecha'] = fecha_tag.text.strip() if fecha_tag else "Fecha no disponible"

        numeros_tag = item.find_all('span', class_='score')
        loteria['numeros'] = [n.text.strip() for n in numeros_tag]

        img_tag = item.find('img', class_='lazy')
        src = img_tag.get('data-src') if img_tag else None
        loteria['imagen'] = f"https://loteriasdominicanas.com{src}" if src and src.startswith('/') else (src or "https://via.placeholder.com/100")

        loterias.append(loteria)

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return loterias, timestamp

def agrupar_loterias(loterias):
    grupos = {
        "Nacional": [],
        "Leidsa": [],
        "Loteka": [],
        "Lotería Real": [],
        "La Primera": [],
        "New York": [],
        "Otras": []
    }
    for l in loterias:
        nombre = l['nombre'].lower()
        if "nacional" in nombre:
            grupos["Nacional"].append(l)
        elif "leidsa" in nombre:
            grupos["Leidsa"].append(l)
        elif "loteka" in nombre:
            grupos["Loteka"].append(l)
        elif "real" in nombre:
            grupos["Lotería Real"].append(l)
        elif "primera" in nombre:
            grupos["La Primera"].append(l)
        elif "new york" in nombre:
            grupos["New York"].append(l)
        else:
            grupos["Otras"].append(l)
    return grupos

@app.route("/")
def home():
    loterias, actualizacion = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    return render_template("resultados.html", grupos=grupos, actualizacion=actualizacion)



def guardar_historial(loterias, timestamp):
    with open("historial.json", "a", encoding="utf-8") as f:
        registro = { "fecha": timestamp, "datos": loterias }
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    loterias, timestamp = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    html = crear_html(grupos)

    with open("resultados.html", "w", encoding="utf-8") as f:
        f.write(html)

    guardar_historial(loterias, timestamp)

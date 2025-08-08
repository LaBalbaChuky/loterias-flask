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
        "Nacional": [], "Leidsa": [], "Real": [], "Loteka": [],
        "Americanas": [], "Primera": [], "La Suerte": [],
        "LoteDom": [], "King Lottery": [], "Anguila": [], "Otras": []
    }

    for l in loterias:
        nombre = l['nombre'].lower()
        if any(x in nombre for x in ["nacional", "juega +", "pega +", "gana más"]):
            grupos["Nacional"].append(l)
        elif any(x in nombre for x in ["leidsa", "pega 3 más", "loto pool", "super kino", "quiniela leidsa", "loto más"]):
            grupos["Leidsa"].append(l)
        elif any(x in nombre for x in ["real", "quiniela real", "loto real"]):
            grupos["Real"].append(l)
        elif any(x in nombre for x in ["loteka", "mega chances"]):
            grupos["Loteka"].append(l)
        elif any(x in nombre for x in ["new york", "florida", "mega millions", "powerball"]):
            grupos["Americanas"].append(l)
        elif any(x in nombre for x in ["primera", "loto 5"]):
            grupos["Primera"].append(l)
        elif any(x in nombre for x in ["la suerte"]):
            grupos["La Suerte"].append(l)
        elif any(x in nombre for x in ["lotedom", "quemaito"]):
            grupos["LoteDom"].append(l)
        elif any(x in nombre for x in ["king lottery"]):
            grupos["King Lottery"].append(l)
        elif any(x in nombre for x in ["anguila"]):
            grupos["Anguila"].append(l)
        else:
            grupos["Otras"].append(l)

    return grupos

def guardar_historial(loterias, timestamp):
    with open("historial.json", "a", encoding="utf-8") as f:
        registro = { "fecha": timestamp, "datos": loterias }
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

# scraper.py

def crear_html(grupos, actualizacion):
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Resultados de Hoy RD</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #0056b3;
                color: white;
                padding: 10px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }}
            .grupo {{
                margin: 20px;
                padding: 15px;
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h2 {{
                background-color: #e6e6e6;
                padding: 8px;
                border-radius: 4px;
            }}
            .loteria {{
                padding: 5px 0;
                border-bottom: 1px solid #ccc;
            }}
        </style>
    </head>
    <body>
        <header>Resultados de Hoy RD</header>
        <p style="text-align:center;">Última actualización: {actualizacion}</p>
    """
    for nombre_grupo, lotos in grupos.items():
        html += f"<div class='grupo'><h2>{nombre_grupo}</h2>"
        for loteria in lotos:
            numeros = " - ".join(loteria['numeros'])
            html += f"<div class='loteria'>{loteria['nombre']} ({loteria['fecha']}): {numeros}</div>"
        html += "</div>"
    html += "</body></html>"
    return html


def guardar_html(html):
    import os
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML generado correctamente en public/index.html")




if __name__ == "__main__":
    loterias, timestamp = obtener_resultados()
    grupos = agrupar_loterias(loterias)

    # ✅ Crear carpeta si no existe
    import os
    os.makedirs("public", exist_ok=True)

    # ✅ Crear el HTML con los resultados
    html = crear_html(grupos, timestamp)

    # ✅ Guardarlo en public/index.html
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)






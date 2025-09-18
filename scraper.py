from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os

# ===================== SCRAPER =====================
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

        loterias.append(loteria)

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return loterias, timestamp

# ===================== AGRUPACIÓN =====================
def agrupar_loterias(loterias):
    grupos = {
        "Nacional": [],
        "Leidsa": [],
        "Real": [],
        "Loteka": [],
        "Americanas": [],
        "Primera": [],
        "La Suerte": [],
        "LoteDom": [],
        "King Lottery": [],
        "Anguila": [],
        "Otras": []
    }

    for l in loterias:
        nombre = l['nombre'].lower()
        if "nacional" in nombre:
            grupos["Nacional"].append(l)
        elif "leidsa" in nombre:
            grupos["Leidsa"].append(l)
        elif "real" in nombre:
            grupos["Real"].append(l)
        elif "loteka" in nombre:
            grupos["Loteka"].append(l)
        elif any(x in nombre for x in ["new york", "florida", "mega millions", "powerball"]):
            grupos["Americanas"].append(l)
        elif "primera" in nombre:
            grupos["Primera"].append(l)
        elif "suerte" in nombre:
            grupos["La Suerte"].append(l)
        elif "lote" in nombre:
            grupos["LoteDom"].append(l)
        elif "king" in nombre:
            grupos["King Lottery"].append(l)
        elif "anguila" in nombre:
            grupos["Anguila"].append(l)
        else:
            grupos["Otras"].append(l)
    return grupos

# ===================== HTML BONITO =====================
def crear_html(grupos, actualizacion):
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Resultados de Hoy RD</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #f4f6f8;
                margin: 0;
                padding: 0;
            }}
            header {{
                background: linear-gradient(to right, #004aad, #0066cc);
                text-align: center;
                padding: 20px 0;
                color: white;
                font-size: 26px;
                font-weight: bold;
            }}
            p.actualizacion {{
                text-align: center;
                color: #333;
                font-size: 14px;
                margin: 10px 0;
            }}
            .grupo-loteria {{
                background: #fff;
                margin: 20px auto;
                max-width: 1100px;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}
            .grupo-loteria h2 {{
                color: #004aad;
                border-left: 4px solid #0077ff;
                padding-left: 10px;
                margin-bottom: 15px;
            }}
            .tarjeta {{
                background: #f9fbfe;
                border-radius: 8px;
                padding: 12px;
                margin: 10px;
                width: 220px;
                display: inline-block;
                vertical-align: top;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .tarjeta h3 {{
                margin: 0;
                color: #007bff;
                font-size: 18px;
            }}
            .tarjeta .fecha {{
                font-size: 13px;
                color: #666;
                margin-bottom: 10px;
            }}
            .numeros {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 6px;
            }}
            .bola {{
                background: #fbc02d;
                border-radius: 50%;
                width: 36px;
                height: 36px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <header>Resultados de Hoy RD</header>
        <p class="actualizacion">Última actualización: {actualizacion}</p>
    """

    for nombre_grupo, lotos in grupos.items():
        if not lotos:
            continue
        html += f"<div class='grupo-loteria'><h2>{nombre_grupo}</h2>"
        for loteria in lotos:
            numeros = "".join(f"<div class='bola'>{n}</div>" for n in loteria['numeros'])
            html += f"""
            <div class="tarjeta">
                <h3>{loteria['nombre']}</h3>
                <p class="fecha">{loteria['fecha']}</p>
                <div class="numeros">{numeros}</div>
            </div>
            """
        html += "</div>"

    html += "</body></html>"
    return html

# ===================== GUARDAR =====================
def guardar_html(html):
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML generado correctamente en public/index.html")


# ===================== EJECUCIÓN LOCAL =====================
if __name__ == "__main__":
    loterias, actualizacion = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    html = crear_html(grupos, actualizacion)
    guardar_html(html)

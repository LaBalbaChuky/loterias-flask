from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os


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
        elif "new york" in nombre or "florida" in nombre or "power" in nombre or "mega" in nombre:
            grupos["Americanas"].append(l)
        elif "primera" in nombre:
            grupos["Primera"].append(l)
        elif "suerte" in nombre:
            grupos["La Suerte"].append(l)
        elif "lotedom" in nombre or "quemaito" in nombre:
            grupos["LoteDom"].append(l)
        elif "king" in nombre:
            grupos["King Lottery"].append(l)
        elif "anguila" in nombre:
            grupos["Anguila"].append(l)
        else:
            grupos["Otras"].append(l)

    return grupos


def crear_html(grupos, actualizacion):
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultados de Hoy RD</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f4f6f8; margin: 0; padding: 0; }}
        header {{ background: linear-gradient(to right, #004aad, #0066cc); text-align: center; padding: 25px 0; }}
        header img {{ width: 280px; max-width: 95%; height: auto; }}

        .grupo-loteria {{ background: #fff; margin: 30px auto; max-width: 1100px; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }}
        .company-title {{ font-size: 22px; font-weight: bold; color: #004aad; margin-bottom: 15px; border-left: 4px solid #0077ff; padding-left: 10px; }}

        .contenedor-loterias {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
        .tarjeta {{ background: white; border-radius: 12px; width: 250px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); padding: 16px; text-align: center; }}
        .tarjeta img {{ height: 50px; object-fit: contain; margin-bottom: 10px; }}
        .tarjeta h3 {{ font-size: 18px; color: #007bff; margin: 0; }}
        .tarjeta .fecha {{ font-size: 14px; color: #555; margin-bottom: 10px; }}
        .numeros {{ display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }}
        .bola {{ background: #fbc02d; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: bold; }}
    </style>
</head>
<body>

<header>
    <img src="logo.png" alt="Resultados de Hoy RD">
    <p style="color:white; margin-top:10px;">Última actualización: {actualizacion}</p>
</header>
"""

    for grupo, lotes in grupos.items():
        if not lotes:
            continue
        html += f'<div class="grupo-loteria">'
        html += f'<div class="company-title">{grupo}</div>'
        html += '<div class="contenedor-loterias">'
        for l in lotes:
            html += f"""
            <div class="tarjeta">
                <img src="{l['imagen']}" alt="{l['nombre']}">
                <h3>{l['nombre']}</h3>
                <p class="fecha">{l['fecha']}</p>
                <div class="numeros">
                    {''.join(f'<div class="bola">{n}</div>' for n in l['numeros'])}
                </div>
            </div>
            """
        html += '</div></div>'

    html += '</body></html>'
    return html


def guardar_html(html):
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ HTML generado correctamente en public/index.html")


def guardar_historial(loterias, timestamp):
    with open("historial.json", "a", encoding="utf-8") as f:
        registro = {"fecha": timestamp, "datos": loterias}
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

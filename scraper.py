import requests
from bs4 import BeautifulSoup

def main():
    url = "https://loteriasdominicanas.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    loterias = []

    for item in soup.find_all('div', class_='game-block'):
        loteria = {}

        # Nombre
        nombre_tag = item.find('a', class_='game-title')
        loteria['nombre'] = nombre_tag.text.strip() if nombre_tag else "Nombre no disponible"

        # Fecha
        fecha_tag = item.find('div', class_='session-date')
        loteria['fecha'] = fecha_tag.text.strip() if fecha_tag else "Fecha no disponible"

        # Números
        numeros_tag = item.find_all('span', class_='score')
        loteria['numeros'] = [n.text.strip() for n in numeros_tag]

        # Imagen (usa src o data-src y completa la URL si es relativa)
        img_tag = item.find('img', class_='lazy')  # Asegúrate de que 'lazy' es la clase correcta
        src = img_tag.get('data-src') if img_tag else None
        if src:
            # Asegúrate de completar la URL si es relativa
            loteria['imagen'] = f"https://loteriasdominicanas.com{src}" if src.startswith('/') else src
        else:
            loteria['imagen'] = "https://via.placeholder.com/100"

        loterias.append(loteria)

    # Crear HTML bonito con estilo de bolas
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Resultados de Loterías</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #f7f9fb;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #222;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
            }
            .loteria-block {
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                width: 280px;
                padding: 15px;
                position: relative;
                transition: transform 0.2s;
            }
            .loteria-block:hover {
                transform: translateY(-5px);
            }
            .fecha-box {
                position: absolute;
                top: 10px;
                right: 10px;
                background: #e0e0e0;
                color: #333;
                padding: 4px 10px;
                border-radius: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            .game-logo {
                width: 100%;
                max-height: 100px;
                object-fit: contain;
                margin-bottom: 10px;
            }
            .game-title {
                font-size: 18px;
                font-weight: bold;
                margin: 5px 0 10px 0;
                color: #007bff;
                text-align: center;
            }
            .game-scores {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: center;
            }
            .score {
                width: 40px;
                height: 40px;
                background: #ffcc00;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 16px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <h1>Resultados de Loterías</h1>
        <div class="container">
    """

    for l in loterias:
        html += f"""
            <div class="loteria-block">
                <div class="fecha-box">{l['fecha']}</div>
                <img src="{l['imagen']}" alt="{l['nombre']}" class="game-logo">
                <div class="game-title">{l['nombre']}</div>
                <div class="game-scores">
                    {''.join(f'<div class="score">{n}</div>' for n in l['numeros'])}
                </div>
            </div>
        """

    html += """
        </div>
    </body>
    </html>
    """

    # Guardar el HTML generado
    with open("templates/resultados.html", "w", encoding="utf-8") as f:
        f.write(html)

# Solo ejecutar la función main si este archivo se ejecuta directamente
if __name__ == "__main__":
    main()

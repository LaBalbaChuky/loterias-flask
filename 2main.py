from scraper import obtener_resultados, agrupar_loterias, crear_html, guardar_html

if __name__ == "__main__":
    loterias, actualizacion = obtener_resultados()
    grupos = agrupar_loterias(loterias)
    html = crear_html(grupos, actualizacion)
    guardar_html(html)

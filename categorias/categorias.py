from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

requests = requests.session()

web = requests.get('https://www.amazon.es/gp/site-directory?ref_=nav_em__fullstore_0_1_1_35', headers=headers)

soup = BeautifulSoup(web.text, 'lxml')

BASE_URL = 'https://www.amazon.es'

categorias_lista = soup.find_all("div", class_="popover-grouping")

exclusiones = ["Amazon Prime Video", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas"]

categorias_info = []

for categorias in categorias_lista:
    categorias_terminado = {}
    titulo = categorias.find("h2")
    validador = any(titulo.text in exclusion for exclusion in exclusiones)
    if validador:
        continue
    else:
        categorias_validas = titulo.parent
        categorias_validas_titulo = categorias_validas.find("h2").text
        links_list = categorias_validas.find_all("a")
        #print(categorias_validas_titulo)
        links_info = []
        for link in links_list:
            #print(link['href'])
            subcategoria = {}
            #print('  └ ─ ' + link.text)
            #print('    └ ─ ' + BASE_URL + link['href'])
            subcategoria['titulo'] = link.text
            subcategoria['link'] = BASE_URL + link['href']
            links_info.append(subcategoria)
        categorias_terminado['titulo_principal'] = titulo.text
        categorias_terminado['subcategoria'] = links_info
        categorias_info.append(categorias_terminado)
    #titulo = categorias.find("h2", class_="popover-category-name").text
print(categorias_info)
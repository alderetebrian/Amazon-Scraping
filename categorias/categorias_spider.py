from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

requests = requests.session()

web = requests.get('https://www.amazon.es/gp/site-directory?ref_=nav_em__fullstore_0_1_1_35', headers=headers)

BASE_URL = 'https://www.amazon.es'

def json_categorias_info():
    soup = soup_file(web)
    sub_categoria = []
    categorias_infos = []
    all_categorias = get_all_categorias(soup)
    categorias = excluir_categorias(all_categorias)
    for categoria in categorias:
        categorias_terminado = {}
        titulo = categoria.find("h2").text
        links_list = categoria.find_all("a") 
        sub_categoria = get_all_sub_categorias(links_list)
        categorias_terminado['titulo_principal'] = titulo
        categorias_terminado['subcategoria'] = sub_categoria
        categorias_infos.append(categorias_terminado)
    return categorias_infos

def soup_file(get_Response):
    soup = BeautifulSoup(get_Response.text, 'lxml')
    return soup

def get_all_categorias(soup):
    categorias_lista = soup.find_all("div", class_="popover-grouping")
    return categorias_lista

def excluir_categorias(categorias):
    exclusiones = ["Amazon Prime Video", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas"]
    categorias_info = []
    for categoria in categorias:
        categorias_terminado = {}
        titulo = categoria.find("h2")
        validador = any(titulo.text in exclusion for exclusion in exclusiones)
        if validador:
            continue
        else:
            categorias_validas = titulo.parent
            categorias_validas_titulo = categorias_validas.find("h2").text
            links_list = categorias_validas.find_all("a")
            categorias_info.append(categorias_validas)
    return categorias_info

def get_all_sub_categorias(links_list):
    links_info = []
    for link in links_list:
        subcategoria = {}
        subcategoria['titulo'] = link.text
        subcategoria['link'] = BASE_URL + link['href']
        links_info.append(subcategoria)
    return links_info

print(json_categorias_info())
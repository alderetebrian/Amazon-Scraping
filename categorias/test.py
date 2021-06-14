from bs4 import BeautifulSoup
import requests
import json
from time import sleep
import random

BASE_URL = 'https://www.amazon.es'

api = requests.session()

def requests_web(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    web = requests.get(url, headers=headers)
    return web
    '''
    sleep(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    proxys = ['109.245.239.125:35659', '161.202.226.194:80', '162.214.92.202:80','79.115.245.227:8080']
    while(True):
        try:
            requests.proxies = random.choice(proxys)
            web = api.get(url, headers=headers, verify=False)
            print(web.status_code)
            if web.status_code == 200:
                break
            elif web.status_code == 404:
                print(url)
                print('Buscando nuevo proxy...')
                requests.proxies = random.choice(proxys)
        except requests.exceptions.RequestException as error: 
            print('Buscando nuevo proxy...')
            requests.proxies = random.choice(proxys)
            print("Error: ", error)
    return web
    '''

def soup_file(get_Response):
    soup = BeautifulSoup(get_Response.text, 'lxml')
    return soup

def get_all_categorias(soup):
    categorias_lista = soup.find_all("div", class_="popover-grouping")
    return categorias_lista

def excluir_categorias(categorias):
    exclusiones = ["Amazon Prime Video", "Amazon Music", "Amazon Photos", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas", "E-readers y eBooks Kindle", "Juguetes y Bebé", "Alimentación y bebidas", "Moda", "Handmade", "Amazon Launchpad"]
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

def categorias_info():
    web = requests_web('https://www.amazon.es/gp/site-directory?ref_=nav_em__fullstore_0_1_1_35')
    soup = soup_file(web)
    sub_categoria_2 = []
    sub_categoria = []
    categorias_infos = []
    categorias_terminado = {}
    print('Obteniendo Categorias...')
    all_categorias = get_all_categorias(soup)
    print('Quitando categorias no necesarias...')
    categorias = excluir_categorias(all_categorias)
    for categoria in categorias:
        print('Accediendo a categoria...')
        titulo = categoria.find("h2").text
        print(f'Extrayendo subcategorias de {titulo}...')
        links_list = categoria.find_all("a") 
        sub_categoria = get_all_sub_categorias(links_list)

        categoria_json = {}
        for link in sub_categoria:
            titulo = link['titulo']
            print(f'Accediendo a subcategoria {titulo}...')
            sub_categoria_2 = get_sub_categoria(link['link'])
            if sub_categoria_2:
                categoria_json['titulo'] = titulo
                categoria_json['sub_categoria'] = sub_categoria_2
                sub_categoria_2.append(categoria_json)
            else:
                print('No subcategoria detectada...')
        
    categorias_terminado['titulo_principal'] = titulo
    categorias_terminado['sub_categoria'] = sub_categoria
    categorias_terminado['sub_categoria']['sub_categoria_2'] = sub_categoria_2
    categorias_infos.append(categorias_terminado)
    return categorias_infos

def get_all_sub_categorias(links_list):
    links_info = []
    for link in links_list:
        subcategoria = {}
        subcategoria['titulo'] = link.text
        subcategoria['link'] = BASE_URL + link['href']
        links_info.append(subcategoria)
    return links_info

def get_sub_categoria(url):
    web = requests_web(url)
    soup = soup_file(web)
    try:
        categorias = soup.find("div", class_="left_nav browseBox")
        categorias_titulos = categorias.find_all("h3")
        sub_categorias = categorias.find_all("a")
        sub_categorias_info = []
        for sub_categoria in sub_categorias:
            json_data = {}
            json_data['titulo'] = sub_categoria.text
            json_data['link'] = BASE_URL + sub_categoria['href']
            json_data['sub_categoria_2'] = {}
            sub_categorias_info.append(json_data)
        return sub_categorias_info
    except:
        print("error")

def get_departamento_categorias(url):
    web = requests_web(url)
    soup = soup_file(web)
    categoria_base = soup.find_all("span", class_="a-size-base a-color-base a-text-bold")
    for categorias in categoria_base:
        categorias_titulo = categorias.text
        if categorias_titulo == 'Departamento':
            categoria_padre = categorias.parent.parent
            sub_categorias = categoria_padre.find_all("a")
            sub_categorias_info = []
            for sub_categoria in sub_categorias:
                json_data = {}
                json_data['titulo'] = sub_categoria.text.strip()
                json_data['link'] = BASE_URL + sub_categoria['href']
                sub_categorias_info.append(json_data)
            print(sub_categorias_info)


print(categorias_info())
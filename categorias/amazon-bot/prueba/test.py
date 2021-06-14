from amazon_config import(
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    DIRECTORY,
    BASE_URL,
    URL_TESTING
)

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
import time
import os

class AmazonAPI:
    def __init__(self, test_url, base_url):
        self.base_url = base_url
        self.test_url = test_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)

    def run(self):
        #data = self.get_categorias("https://www.amazon.es/dp/B07PFG54H7/259-7320413-3885138?_encoding=UTF8&ref_=sd_allcat_k_echo_cs")
        #print(data)
        json_base = self.json_base()
        self.search_all_urls(json_base)
        self.driver.quit()

    def analizar(self, data):
        for key, value in data.items():
            if key == 'flag' and value == False:
                if key == 'sub_categoria' and value != '':
                    data['flag'] = True
                try:              
                    for link in data['sub_categoria']:
                        #print('actualmente en:')
                        #print(link['titulo'])
                        verificar = self.get_categorias(link['link'])
                        if verificar:
                            link['sub_categoria'] = verificar
                            print('categoria nueva añadida')
                            return data
                        #print(link['titulo'])
                    #print(data['link'])
                    #print(data['link'])
                except:
                    return data

            elif type(value) is list:
                for item in value:
                    if type(item) is dict:
                        self.analizar(item)

    def search_all_urls(self, json_base):
        for data in json_base:
            print('\n\n')
            terminado = self.analizar(data)
            #guardar = self.create_json(terminado)
            print(terminado)
            print('json_base modificado')
    '''
    def search_all_urls(self, json_base):
        for data in json_base:
            print('\n\n')
            terminado = self.analizar(data)
            self.create_json(terminado)
        #export = json.dumps(json_base)
            print('json_base modificado')
        #self.makeJson('json_base',export)
    '''
    '''
    
    def create_json(self, archivo_json):
            lista = []
            for data in archivo_json:
                    json_file = self.analizar(data)
                    lista.append(json_file)
            self.makeJson_base('prueba', lista)
            json_load = self.loadJson('prueba')
            self.create_json(json_load)
            return lista
    '''

    def makeJson_base(self, name,element):
        print('json creado')
        with open(f'{name}.json', 'w') as outfile:  
            json.dump(element, outfile)

    def makeJson(self,name,element):
        if not os.path.isfile(f'{name}.json') or os.stat(f'{name}.json').st_size == 0:
            print('Creando json_base...')
            with open(f'{name}.json', 'w') as outfile:  
                json.dump(element, outfile)
        else:
            print('json_base ya creado...')
            print('cargando json_base...')
            json_base = self.loadJson('json_base')
            return json_base
 

    def loadJson(self,name):
        with open(f'{name}.json') as json_file:
            data = json.load(json_file)
            return data

    def json_base(self):
        self.driver.get(URL_TESTING)
        soup = self.soup_file()
        print('Buscando categorias en Amazon...')
        time.sleep(5)
        all_categorias = self.get_all_categorias(soup)
        print(f'Numero de categorias encontradas: {len(all_categorias)}')
        print(f'Quitando categorias excluidas...')
        time.sleep(4)
        categorias = self.excluir_categorias(all_categorias)
        print(f'Numero de categorias actual: {len(categorias)}')
        time.sleep(10)
        sub_categorias = self.categorias_principal(categorias)
        json_data = self.makeJson('json_base',sub_categorias)
        return json_data

    def get_all_categorias(self, soup):
        categorias_lista = soup.find_all("div", class_="popover-grouping")
        return categorias_lista

    def excluir_categorias(self, categorias):
        exclusiones = ["Amazon Prime Video", "Amazon Music", "Amazon Photos", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas", "E-readers y eBooks Kindle", "Juguetes y Bebé", "Alimentación y bebidas", "Moda", "Handmade", "Amazon Launchpad"]
        categorias_info = []
        for categoria in categorias:
            titulo = categoria.find("h2")
            validador = any(titulo.text in exclusion for exclusion in exclusiones)
            if validador:
                continue
            else:
                categorias_validas = titulo.parent
                categorias_info.append(categorias_validas)
        return categorias_info

    def categorias_principal(self, categorias):
        lista_categorias = []
        for categoria in categorias:
            titulo = categoria.find("h2").text.strip()
            links_list = categoria.find_all("a") 
            sub_categoria = self.get_all_sub_categorias(links_list)
    
            categoria_terminada = {
                'titulo_principal': titulo,
                'sub_categoria': sub_categoria,
                'flag': False
            }
    
            lista_categorias.append(categoria_terminada)
        json_data = json.dumps(lista_categorias)
        return lista_categorias

    def get_all_sub_categorias(self, links_list):
        links_info = []
        for link in links_list:
            subcategoria = {}
            subcategoria['titulo'] = link.text.strip()
            subcategoria['link'] = BASE_URL + link['href']
            subcategoria['sub_categoria'] = ''
            subcategoria['flag'] = False
            links_info.append(subcategoria)
    
        return links_info

    def get_categorias(self, url):
        time.sleep(6)
        #pasa categoria por categoria, en caso de no encontrar nada devolveria None lo cual significa que seria el final.
        self.driver.get(url)
        soup = self.soup_file()
        try:
            left_categorias = soup.find("div", class_='a-column a-span12 apb-browse-left-nav apb-browse-col-pad-right a-span-last')
            get_links = left_categorias.select('a[href*="node="]')

            links_info = []
            for link in get_links:
                if link.find("span", class_="apb-browse-back-arrow-icon aok-inline-block"):
                    continue
                else:
                    titulo = link.text.strip()
                    sub_link = BASE_URL + link['href']
                    subcategoria = {}
                    subcategoria['titulo'] = titulo
                    subcategoria['link'] = sub_link
                    subcategoria['sub_categoria'] = ''
                    subcategoria['flag'] = False
                    
                    print(titulo)
                    links_info.append(subcategoria)
                    #print(sub_link)
            print(links_info)
            return links_info
        except Exception as e:
            print(e)

    def soup_file(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup

if __name__ == "__main__":
    print("HEY!!!")
    amazon = AmazonAPI(URL_TESTING, BASE_URL)
    data = amazon.run()
    print(data)

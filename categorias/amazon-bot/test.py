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
        self.json_base()
        prueba = self.verificar_categoria(sub_categorias)
        #print(sub_categorias)
        self.driver.quit()

    def makeJson(self,name,element):
        with open(f'{name}.json', 'w') as outfile:  
            json.dump(element, outfile)

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

    def get_all_categorias(self, soup):
        categorias_lista = soup.find_all("div", class_="popover-grouping")
        return categorias_lista

    def excluir_categorias(self, categorias):
        exclusiones = ["Amazon Prime Video", "Amazon Music", "Amazon Photos", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas", "E-readers y eBooks Kindle", "Juguetes y Beb??", "Alimentaci??n y bebidas", "Moda", "Handmade", "Amazon Launchpad"]
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

            for link in get_links:
                if link.find("span", class_="apb-browse-back-arrow-icon aok-inline-block"):
                    continue
                else:
                    titulo = link.text.strip()
                    sub_link = BASE_URL + link['href']
                    print(titulo)
                    #print(sub_link)
        except Exception as e:
            print(e)

    def verificar_categoria(self, categorias):
        time.sleep(6)
        sub_categoria = []
        for categoria in categorias:
            for link in categoria['sub_categoria']:
                print(link['link'])
                verificar = self.get_categorias(link['link'])
                sub_categoria.append(verificar)
        print(sub_categoria)
        return sub_categoria

    def soup_file(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup

if __name__ == "__main__":
    print("HEY!!!")
    amazon = AmazonAPI(URL_TESTING, BASE_URL)
    data = amazon.run()
    print(data)

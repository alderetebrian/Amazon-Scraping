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

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, test_url, base_url):
        self.base_url = base_url
        self.test_url = test_url
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)

    def run(self):
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
        #arreglar categorias
        sub_categorias = self.verificar_sub_categoria_1(categorias)
        time.sleep(14)
        sub_categorias_2 = self.verificar_sub_categoria_2(sub_categorias)
       # sub_categorias_2 = self.verificar_sub_categoria_2_simple('https://www.amazon.es/tablets/b?ie=UTF8&node=938010031&ref_=sd_allcat_tab')
        print(sub_categorias_2)
        self.driver.quit()

    def soup_file(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup

    def get_all_categorias(self, soup):
        categorias_lista = soup.find_all("div", class_="popover-grouping")
        return categorias_lista

    def excluir_categorias(self, categorias):
        exclusiones = ["Amazon Prime Video", "Amazon Music", "Amazon Photos", "Appstore para Android", "Amazon Business", "Cheques Regalo y Recargas", "E-readers y eBooks Kindle", "Juguetes y Bebé", "Alimentación y bebidas", "Moda", "Handmade", "Amazon Launchpad"]
        categorias_info = []
        for categoria in categorias:
            #categorias_terminado = {}
            titulo = categoria.find("h2")
            validador = any(titulo.text in exclusion for exclusion in exclusiones)
            if validador:
                continue
            else:
                categorias_validas = titulo.parent
                #categorias_validas_titulo = categorias_validas.find("h2").text
                #links_list = categorias_validas.find_all("a")
                categorias_info.append(categorias_validas)
        return categorias_info

    def verificar_sub_categoria_1(self, categorias):
        lista_categorias = []
        for categoria in categorias:
            titulo = categoria.find("h2").text
            print(f"\nTitulo principal: {titulo}")
            links_list = categoria.find_all("a") 
            sub_categoria = self.get_all_sub_categorias(links_list)
            print("  └─ " + f"Cantidad Subcategorias: {len(sub_categoria)}")
            for titulo in sub_categoria:
                print("  └─ " + titulo['titulo'])
            lista_categorias.append(sub_categoria)
        return lista_categorias

    def verificar_sub_categoria_2_simple(self, url):
        sub_categoria = []
        normal = self.get_sub_categoria(url)
        departamento = self.get_departamento_categorias(url)
        sub_categoria_2 = {}

        if normal == None: normal = ''
        if departamento == None: departamento = ''
        '''
        if normal == None:
            normal = ''
                
        if departamento == None:
            departamento = ''
        '''
        sub_categoria_2['categoria_normal'] = normal
        sub_categoria_2['categoria_departamento'] = departamento
        sub_categoria.append(sub_categoria_2)
        return sub_categoria        

    def verificar_sub_categoria_2(self, categorias):
        time.sleep(6)
        sub_categoria = []
        for categoria in categorias:
            for elemento in categoria:
                verificar = self.verificar_sub_categoria_2_simple(elemento['link'])
                print(verificar)
                sub_categoria.append(verificar)
        print(sub_categoria)
        return sub_categoria

    def get_all_sub_categorias(self, links_list):
        links_info = []
        for link in links_list:
            subcategoria = {}
            subcategoria['titulo'] = link.text.strip()
            subcategoria['link'] = BASE_URL + link['href']
            links_info.append(subcategoria)

        return links_info
    
    def get_sub_categoria(self, url):
        time.sleep(16)
        self.driver.get(url)
        soup = self.soup_file()
        json_terminado = []
        try:
            categorias = soup.find("div", class_="left_nav browseBox")
            categorias_titulos = categorias.find_all("h3")
            get_all_ul = categorias.find_all("ul")

            for index, categoria in enumerate(get_all_ul):
                sub_categorias_info = []
                principal_json = {}
                titulo = categorias_titulos[index]
                sub_categorias = categoria.find_all("a")

                principal_json['principal_titulo'] = titulo.text
                principal_json['sub_categorias'] = sub_categorias_info
                json_terminado.append(principal_json)
                for sub_categoria in sub_categorias:
                    json_data = {}
                    sub_categoria_titulo = sub_categoria.text
                    link = BASE_URL + sub_categoria['href']
                    json_data['titulo'] = sub_categoria_titulo
                    json_data['link'] = link
                    sub_categorias_info.append(json_data)
            return json_terminado
        except Exception as e:
            print(e)

    def get_departamento_categorias(self, url):
        time.sleep(10)
        self.driver.get(url)
        soup = self.soup_file()
        try:
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
                return sub_categorias_info
        except Exception as e:
            print(e)
   

        

if __name__ == "__main__":
    print("HEY!!!")
    amazon = AmazonAPI(URL_TESTING, BASE_URL)
    data = amazon.run()
    print(data)

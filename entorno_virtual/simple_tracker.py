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
        print("Starting script...")
        print(f"Looking for products...")
        links = self.get_products_links()
        links = links["product_links"]
        time.sleep(3)
        if not links:
            print("Stopped script.")
            return
        print(f"got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()
        return products

    def get_products_links(self):
        self.driver.get(self.test_url)

        product_links = []
        try:
            soup = self.soup_file()
            product_info = soup.find_all("div", {"class": "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"})
            product_asins = [product["data-asin"] for product in product_info]
            product_links = [link.find("a", {"class": "a-link-normal a-text-normal"})["href"] for link in product_info]
            return {"product_asins": product_asins, "product_links": product_links}
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return product_links

    def soup_file(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup
        
    def get_products_info(self, links):
        asins = self.get_products_links()
        asins = asins["product_asins"]
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products

    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?language=es')
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()

        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            soup = self.soup_file()
            return (soup.find("span", id="productTitle").text).strip()
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None
    
    def get_seller(self):
        try:
            soup = self.soup_file()
            return (soup.find("a", {"id": "bylineInfo"}).text)
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        return ''
        '''
        price = None
        try:
            soup = self.soup_file()
            price = soup.find(id="priceblock_ourprice").text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = soup.find(id="availability").text
                if 'Available' in availability:
                    price = soup.find(class_="olp-padding-right").text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price
        '''

    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin

    def convert_price(self, price):
        price = price.split(self.currency)[1]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        try:
            price = price.split(",")[0] + price.split(",")[1]
        except:
            Exception()
        return float(price)

'''
    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]
'''

if __name__ == "__main__":
    print("HEY!!!")
    amazon = AmazonAPI(URL_TESTING, BASE_URL)
    data = amazon.run()
    print(data)

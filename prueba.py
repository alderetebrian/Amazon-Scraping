from selenium import webdriver
from bs4 import BeautifulSoup

BASE_URL = "https://www.amazon.com/"

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

#we create the driver specifying the origin of chrome browser
driver = webdriver.Chrome("./chromedriver.exe", chrome_options=option)

driver.get(f"https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A281407&language=es&ref=nav_em__nav_desktop_sa_intl_accessories_and_supplies_0_2_5_2")
#driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'lxml')
title = soup.find_all("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2")
link = title[0].find("a")['href']
link_terminado = BASE_URL + link
print(title[0].text)
print(link_terminado)
driver.get(link_terminado)
soup = BeautifulSoup(driver.page_source, 'lxml')
title = (soup.find("h1", id="title").text).strip()
price = soup.find("span", id="priceblock_ourprice").text
price_envio = (soup.find("span", class_="a-size-base a-color-secondary").text).strip()
table = soup.find("table", class_="a-normal a-spacing-micro")
table_content = soup.find_all("tr", "a-spacing-small")

print(title)
print(price)
print(price_envio)
print(table_content)
driver.quit()
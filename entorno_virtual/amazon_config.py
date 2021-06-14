from selenium import webdriver

DIRECTORY = 'reports'

URL_TESTING = "https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A281407&language=es&ref=nav_em__nav_desktop_sa_intl_accessories_and_supplies_0_2_5_2"
BASE_URL = "https://www.amazon.com/"

def get_chrome_web_driver(options):
    return webdriver.Chrome('./chromedriver', chrome_options=options)

def get_web_driver_options():
    return webdriver.ChromeOptions()

def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-erros')

def set_browser_as_incognito(options):
    options.add_argument('--incognito')

def set_automation_as_head_less(options):
    options.add_argument('--headless')
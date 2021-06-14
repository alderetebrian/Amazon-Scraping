from selenium import webdriver

DIRECTORY = 'reports'

URL_TESTING = "https://www.amazon.es/gp/site-directory?ref_=nav_em__fullstore_0_1_1_35"
BASE_URL = "https://www.amazon.es"

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
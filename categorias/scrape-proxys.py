import requests
from bs4 import BeautifulSoup
import random
import pandas as pd


#get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

def extract(proxy):
    #this was for when we took a list into the function, without conc futures.
    #proxy = random.choice(proxylist)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        #change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=1)
        print(r.json(), r.status_code)
    except:
        pass
    return proxy

proxylist = getProxies()
#print(len(proxylist))

def proxy_checker(proxylist):
    valid_proxy = []
    for proxy in proxylist:
        requests.proxies = proxy
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        r = requests.get('https://www.amazon.es/', headers=headers)
        if r.status_code == 200:
            print(f"{proxy} - valid")
            valid_proxy.append(proxy)
    return valid_proxy

lista_proxys = proxy_checker(proxylist)

df = pd.DataFrame(lista_proxys, columns=["proxys"])
df.to_csv('proxy-list.csv', index=False)
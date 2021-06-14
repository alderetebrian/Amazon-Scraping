from bs4 import BeautifulSoup
import requests

headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}


def get_links(url):
    response = requests.get(url, headers=headers)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    links = []
    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is not None and link_url.startswith('http'):
            links.append(link_url + '\n')

    write_to_file(links)
    return links


def write_to_file(links):
    with open('data.txt', 'a') as f:
        f.writelines(links)


def get_all_links(url):
    for link in get_links(url):
        get_all_links(link)


r = 'https://www.amazon.es/gp/site-directory?ref_=nav_em__fullstore_0_1_1_35'
write_to_file([r])
get_all_links(r)
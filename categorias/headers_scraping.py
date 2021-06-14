import requests
from bs4 import BeautifulSoup
import pandas as pd

api = requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}

count = 1
list_agent = []
while(count <= 11):
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/' + str(count)
    response = api.get(url, headers=headers)

    soup = BeautifulSoup(response.text,'lxml')
    user_agent = soup.find_all("td", class_="useragent")

    for agent in user_agent:
        list_agent.append(agent.find("a").text)
    count += 1
    print(response.status_code)

df = pd.DataFrame(list_agent, columns=["columns"])
#df.to_csv('headers-list.csv', index=False, sep='\t')
df.to_csv('headers-list.csv', index=False)
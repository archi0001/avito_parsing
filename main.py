from bs4 import BeautifulSoup
import requests

urll = 'https://www.avito.ru/sankt_peterburg_i_lo/noutbuki?cd=1&q=macbook&s=104'
request = requests.get(urll)

bs = BeautifulSoup(request.text, 'html.parser')

all_links = bs.find_all('a', rel="noopener", itemprop="url")
i = 0
for link in all_links:
    if i == 1:
        i = 0
        continue
    print('https://avito.ru' + link["href"])
    i += 1
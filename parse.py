import requests
from bs4 import BeautifulSoup as bs

query = 'Jordi Alba'
URL = f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={query}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(URL, headers=headers)

soup = bs(response.content, "html.parser")

link = soup.select_one(f'td.hauptlink > a[title*="{query}"]')
print(links)
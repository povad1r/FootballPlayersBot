import requests
from bs4 import BeautifulSoup as bs
def get_link(query):
    URL = f'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={query}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(URL, headers=headers)

    soup = bs(response.content, "html.parser")
    first = soup.select_one(f'td.hauptlink > a[title*="{query}"]')
    link = ' https://www.transfermarkt.com' + first.get("href")

    return link

def parse_info(link):
    URL = link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(URL, headers=headers)

    soup = bs(response.content, "html.parser")
    shirt_number = soup.find("span", class_="data-header__shirt-number").get_text(strip=True)
    name_surname = soup.find("strong").get_text(strip=True)
    club = soup.find("span", class_='data-header__club').get_text(strip=True)
    transfer_price = soup.find("a", class_='data-header__market-value-wrapper').get_text(strip=True)
    transfer_price_without_last_update = transfer_price.split("Last update:")[0]
    nationality = soup.find("span", {"itemprop": "nationality"}).get_text(strip=True)
    date_of_birth = soup.find("span", {"itemprop": "birthDate"}).get_text(strip=True)
    player_info = {
        'shirt_number': shirt_number,
        'name_surname': name_surname,
        'club': club,
        'transfer_price': transfer_price_without_last_update,
        'nationality': nationality,
        'date_of_birth': date_of_birth
    }
    return player_info



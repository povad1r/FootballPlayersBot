import requests
from bs4 import BeautifulSoup as bs


def get_link(query):
    print(query)
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
    player_short_info = soup.find("h1", class_='data-header__headline-wrapper').get_text().split()
    shirt_number = player_short_info[0]
    delimiter = ' '
    name_surname = delimiter.join(player_short_info[1:3])
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


def get_player_performance_data(link):
    base_url = "https://www.transfermarkt.com/ceapi/player/"
    full_name = link.split('/')[-1]
    url = f"{base_url}{full_name}/performance"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    games_played = 0
    goals_scored = 0
    assists = 0
    red_cards = 0
    yellow_cards = 0
    for entry in data:
        games_played += entry["gamesPlayed"]
        goals_scored += entry["goalsScored"]
        assists += entry["assists"]
        yellow_cards += entry["yellowCards"]
        red_cards += entry["redCards"]

    statistics = {
        'games_played': games_played,
        'goals_scored': goals_scored,
        'assists': assists,
        'yellow_cards': yellow_cards,
        'red_cards': red_cards
    }

    return statistics

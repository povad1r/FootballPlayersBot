import requests
from bs4 import BeautifulSoup as bs

def get_match_link(link):
    base_url = "https://www.transfermarkt.com/ceapi/nextMatches/player/"
    full_name = link.split('/')[-1]

    url = f"{base_url}{full_name}"
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    matches = data.get("matches", [])
    for match_info in matches:
        match_state = match_info.get("match", {}).get("state", "")
        if match_state != "Played":
            match_id = match_info.get("id")
            return match_id


def get_match_info(match_id):
    url = f'https://www.transfermarkt.com/spielbericht/index/spielbericht/{match_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = bs(response.content, "html.parser")

    match_info = soup.find('div', class_='sb-spieldaten').get_text(strip=True)
    match_info_lines = match_info.split('|')
    date = match_info_lines[1]
    time = match_info_lines[2].split('-')[0].strip()

    home_team = soup.find('div', class_='sb-team sb-heim').get_text(strip=True)
    guest_team = soup.find('div', class_='sb-team sb-gast').get_text(strip=True)
    competition = soup.find('a', class_='direct-headline__link').get_text(strip=True)
    home_team_filter = home_team.split("Position:")[0].strip()
    guest_team_filter = guest_team.split("Position:")[0].strip()

    match = {
        'date': date,
        'time': time,
        'home_team': home_team_filter,
        'guest_team': guest_team_filter,
        'competition': competition
    }
    return match
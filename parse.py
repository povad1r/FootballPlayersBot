from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup as bs


def get_match_link(link):
    driver = webdriver.Chrome()

    driver.get(link)
    try:
        odds_serve_span = driver.find_element(By.CSS_SELECTOR, 'div.quote-slot span.oddsServe')
        data_match = odds_serve_span.get_attribute('data-match')

        print("data-match:", data_match)
        return data_match
    except:
        print("Element not found")

    driver.quit()


def get_match_info(data_match):
    url = f'https://www.transfermarkt.com/spielbericht/index/spielbericht/{data_match}'
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

    home_team_filter = home_team.split("Position:")[0].strip()
    guest_team_filter = guest_team.split("Position:")[0].strip()
    match = {
        'date': date,
        'time': time,
        'home_team': home_team_filter,
        'guest_team': guest_team_filter
    }
    print(match)
    return match



get_match_info(get_match_link('https://www.transfermarkt.com/pepe/profil/spieler/14132'))
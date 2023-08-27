from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup as bs
import time
import arsenic


def get_match_link(link):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Add this line to enable headless mode
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    try:
        odds_serve_span = driver.find_element(By.XPATH,
                                              '//*[@id="main"]/main/div[3]/div[2]/tm-next-matches/div[3]/span')
        data_match = odds_serve_span.get_attribute('data-match')
        return data_match
    except:
        print("Element not found")
    finally:
        driver.quit()

async def get_match_info(data_match):
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



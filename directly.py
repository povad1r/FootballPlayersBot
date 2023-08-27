import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_match_link(link):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Add this line to enable headless mode
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    driver.get(link)

    try:
        wait = WebDriverWait(driver, 10)
        element_text = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/div[3]/div[2]/tm-next-matches/div[2]/div[2]/div[1]/div[0]')))  # Use a relative XPath here
        elementos = element_text.text
        print(elementos)

        return element_text
    except:
        print("Element not found")
    finally:
        driver.quit()


get_match_link('https://www.transfermarkt.com/lionel-messi/profil/spieler/28003')
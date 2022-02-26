import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import unidecode


FORM_LINK = 'https://docs.google.com/forms/d/e/1FAIpQLSf8uYnt0W8iZjwNovOoKBVy8NjjhrrYE_HGAYWYirAKUt7W-Q/viewform?usp=sf_link'
CHROME_DRIVER_PATH = '/Users/kuba/Development/chromedriver'
URL = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?roomsNumber=%5BTWO%5D'

r = requests.get(
    url=URL,
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Accept-Language": "en-US,en;q=0.5"
    }
)
r.raise_for_status()
page = r.text

soup = BeautifulSoup(page, 'html.parser')
all_links_elements = soup.select(selector='#__next > div.css-1i02l4.ee6kzq26 > main > div > div.css-172356e.ee6kzq23 > '
                                          'div.css-7fb6fe.e76enq87 > div.css-1sxg93g.e76enq86 > div '
                                          '> ul li a')
all_links = []

for link in all_links_elements:
    href = link['href']
    if "http" not in href:
        all_links.append(f"https://www.otodom.pl{href}")
    else:
        all_links.append(href)

print(all_links)
all_items_elements = soup.select(selector='#__next > div.css-1i02l4.ee6kzq26 > main > div > div.css-172356e.ee6kzq23 > '
                                          'div.css-7fb6fe.e76enq87 > div.css-1sxg93g.e76enq86 > div > ul li p ')

all_addresses = []
all_prices = []

for item in all_items_elements:
    item = item.getText()
    if 'Warszawa' in item:
        all_addresses.append(item)
    if 'zł' in item:
        item = unidecode.unidecode(item)
        all_prices.append(item)

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

for n in range(len(all_links)):
    driver.get(FORM_LINK)

    time.sleep(2)
    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()
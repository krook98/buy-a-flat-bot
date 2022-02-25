import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
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
                                          'div.css-7fb6fe.e76enq87 > div.css-1sxg93g.e76enq86 > div.css-1dcvyuj.e76enq80 '
                                          '> div > ul li a')
all_links = []
for link in all_links_elements:
    href = link['href']
    if "http" not in href:
        all_links.append(f"https://www.otodom.pl{href}")
    else:
        all_links.append(href)

print(all_links)
all_prices_elements = soup.find_all(class_='css-1bq5zfe es62z2j16')
all_prices = []
for price in all_prices_elements:
    price = price.getText()
    price = unidecode.unidecode(price)
    all_prices.append(price)
print(all_prices)

# all_prices_elements = all_prices_elements[1].getText()
# all_prices = []
# for price in all_prices_elements:
#     all_prices.append(price)
#
# print(all_prices)
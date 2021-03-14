import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException

ZILLOW_URL = 'https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.65614546728516%2C%22east%22%3A-122.21051253271484%2C%22south%22%3A37.65641789561034%2C%22north%22%3A37.89397418197668%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A887983%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'
CHROME_DRIVER_PATH = 'D:\Documents\Projects\chromedriver'
Google_form_url = 'https://forms.gle/fAdtmagv9KbAPhqX6'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
    "Accept-Language": "en-US,en;q=0.9,el;q=0.8",
}

response = requests.get(ZILLOW_URL, headers=headers)
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, "html.parser")
link_list = []
for link in soup.find_all(name="div", class_="list-card-info"):
    link_text = str(link.find(name="a", class_="list-card-link")["href"])
    if not link_text.startswith("https://www.zillow.com"):
        link_text = "https://www.zillow.com" + link_text
    link_list.append(link_text)
# print(link_list)

price_list = []
for x in soup.find_all(name="div", class_="list-card-info"):
    price_text = (x.find(name="div", class_="list-card-price"))
    price_list.append(price_text.text.split(" ")[0])
# print(price_list)

address_list = []
for y in soup.find_all(name="div", class_="list-card-info"):
    address_text = (y.find(class_="list-card-addr"))
    address_list.append(address_text.text)
# print(address_list)

counter = 0

for number in range(len(address_list)):
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(Google_form_url)
    time.sleep(1)
    try:
        first_ques = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        second_ques = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        third_ques = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        submit_button = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')

        first_ques.send_keys(address_list[counter])
        second_ques.send_keys(price_list[counter])
        third_ques.send_keys(link_list[counter])

        counter += 1

        submit_button.click()
    except ElementClickInterceptedException:
        pass
    driver.quit()

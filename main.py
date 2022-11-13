import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(f"https://www.avito.ru/")
text_input = input('введи чё нибудь')
soup = BeautifulSoup(driver.page_source, features="lxml")
info_tags = soup.find_all('span', class_='stat__number')
input_text = driver.find_element('id', 'downshift-input')
button = driver.find_element('class', 'button-textBox-_SF60')
time.sleep(1)
input_text.send_keys(text_input)

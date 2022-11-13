import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())

while True:
    text_input = input("введи чё нибудь:")
    driver.get(f"https://www.avito.ru/saratov?q={text_input}")
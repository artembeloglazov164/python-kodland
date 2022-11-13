import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
driver = webdriver.Chrome(ChromeDriverManager().install())

text_input = input("введи чё нибудь:")
for i in range(1,4):
    driver.get(f"https://www.avito.ru/saratov?p={i}&q={text_input}")
    time.sleep(3)
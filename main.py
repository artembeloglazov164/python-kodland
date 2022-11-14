import re
import time
import replace
from kodland_db import db
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())

text_input = input("введите что искать:")
for i in range(1):
    driver.get(f"https://www.avito.ru/saratov?p={i}&q={text_input}")
    time.sleep(3)
    url = 'https://www.avito.ru'
    soup = BeautifulSoup(driver.page_source, features="lxml")
    blocks = soup.find_all('div', class_=re.compile('iva-item-content'))
    data = []
    for block in blocks:
        data.append({
            'item': block.find('h3', class_=re.compile('title-root')).get_text(strip=True),
            'price': block.find('span', class_=re.compile('price-text')).get_text(strip=True).replace('₽', '').replace('\xa0', ''),
            'city': block.find('a', class_=re.compile('link-link')).get('href').split('/')[1],
            'region': block.find('div', class_=re.compile('geo-root')).get_text(strip=True),
            'link': url + block.find('a', class_=re.compile('link-link')).get('href'),
        })
element = len(data)
print (element)
for i in range(element):        
    db.avito.put(data[i])
print ('Данные записаны в базу')

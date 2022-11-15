import re
import time
import replace
import sqlite3
from kodland_db import db
from flask import Flask, render_template, request, url_for, redirect, jsonify
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())

#Очищаем базу от предыдущих запросов при помощи sqlite3
print('Очищаем базу от предыдущих запросов.')
conn = sqlite3.connect('kodland_db\db.db')
c = conn.cursor()
c.execute('DELETE FROM avito;',);
print('ОК Удалено', c.rowcount, 'записей в таблице.')
conn.commit()
conn.close()

#Вводим данные для поиска
text_input = input("введите что искать:")

#Осуществляем поиск и определяем количество найденых страниц
driver.get(f"https://www.avito.ru/saratov?&q={text_input}")
soup = BeautifulSoup(driver.page_source, features="lxml")
try:
    pages = soup.find('span', {'data-marker': 'pagination-button/next'}).previous_element
except:
    pages = 1
print('По вашему запросу найдено', pages, 'страниц')

#Вводим колличество страниц с которых будем забирать данные а базу
page = int (input ("введите количество страниц для сохранения результатов:"))

#Пробегаем по указанным страницам и парсим данные в списки которые пишем в базу данных 
for i in range(page):
    driver.get(f"https://www.avito.ru/saratov?p={1+i}&q={text_input}")
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
    print ('Найдено', element,'объявлений на странице',1+i)
    for i in range(element):        
        db.avito.put(data[i])
    print ('ОК Данные записаны в базу')

#Подключаемся к базе и выводим количество зписей в консоль    
conn = sqlite3.connect('kodland_db\db.db')
c = conn.cursor()
c.execute('SELECT * FROM avito')
rows = c.fetchall()
print('ОК В базе находится', len(rows), 'записей.')
conn.close()

#Выводим сообщение после завершения кода
print ('код завершил работу без ошибок')

#Создаем веб-приложение
app = Flask(__name__)

@app.route('/')
def avito_searcher():
    data = db.avito.get_all()
    for row in data:
        row.price = row.price
        row.item = row.item
        row.city = row.city
        row.region = row.region
        row.link = row.link
    return render_template('avito.html', data=data)
#Запускаем приложение
if __name__ == "__main__":
    app.run()
    
driver.get(f"http://127.0.0.1:5000")
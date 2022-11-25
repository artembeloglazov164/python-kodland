import re
import time
import replace
import sqlite3
from datetime import datetime, timedelta
from kodland_db import db
from flask import Flask, render_template, request, url_for, redirect, jsonify, session, g
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

########################################################

#Очищаем базу от предыдущих запросов при помощи sqlite3

def db_clean():  
    print('Очищаем базу от предыдущих запросов.')
    conn = sqlite3.connect('kodland_db\db.db')
    c = conn.cursor()
    c.execute('DELETE FROM avito;',);
    print('ОК Удалено', c.rowcount, 'записей в таблице.')
    conn.commit()
    conn.close()
    
########################################################
    
#Получаем данные для поиска из Flask и определяем количество найденных страниц
    
def page_find(text_input):  
    driver = webdriver.Chrome(ChromeDriverManager().install())   
    print('Ищем',text_input)
    driver.get(f"https://www.avito.ru/saratov?&q={text_input}")
    soup = BeautifulSoup(driver.page_source, features="lxml")
    try:
        global pages #Объявляем переменную pages как глобальную
        pages = soup.find('span', {'data-marker': 'pagination-button/next'}).previous_element
    except:
        pages = 1
    print('По вашему запросу найдено', pages, 'страниц')


########################################################
    
#Пробегаем по указанным страницам и парсим данные в списки которые пишем в базу данных
    
def find(text_input,page):
    driver = webdriver.Chrome(ChromeDriverManager().install())    
    for i in range(page):
        driver.get(f"https://www.avito.ru/saratov?p={1+i}&q={text_input}")
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

########################################################
        
#Подключаемся к базе и выводим количество записей в консоль
        
def bd_items():
    conn = sqlite3.connect('kodland_db\db.db')
    c = conn.cursor()    
    c.execute('SELECT * FROM avito')
    rows = c.fetchall()
    print('ОК В базе находится', len(rows), 'записей.')
    conn.close()

#######################################################
#Создаем веб-приложение
    
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        global text_input #Объявляем переменную text_input как глобальную
        text_input = request.form['text_input']
        search_date = datetime.now()
        search_date = search_date.strftime('%Y-%m-%d %H:%M:%S')
        if not text_input:
            return render_template('input.html', message='Вы ничего не ввели')
        db.search.put({"text_input": text_input , "date": search_date})
        db_clean()
        page_find(text_input)
        return render_template('parse.html',message = ('По запросу найдено ' + pages + ' страниц'))
    return render_template('input.html')

@app.route('/parse', methods=['GET', 'POST'])
def parse():
    if request.method == 'POST':
        page = request.form['page']
        if not page:
            return render_template('parse.html', message='Вы ничего не ввели')
        page = int(page)
        find(text_input,page)
        bd_items()
        return redirect(url_for('avito'))
    return render_template('parse.html')


@app.route('/avito', methods=['GET', 'POST'])
def avito():
    data = db.avito.get_all()
    for row in data:
        row.price = row.price
        row.item = row.item
        row.city = row.city
        row.region = row.region
        row.link = row.link
    return render_template('avito.html', data=data)



@app.route('/history')
def history():
    data = db.search.get_all()
    for row in data:
        row.text_input = row.text_input
        row.date = row.date
    return render_template('history.html', data=data)



#Запускаем приложение
if __name__ == "__main__":
    app.run()
 


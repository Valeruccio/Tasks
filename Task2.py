#Загружаем необходимые расширения
#Нам потребуется модуль для работы с ссылками, красивый суп и модуль для подсчетов
import requests
from bs4 import BeautifulSoup
from pandas import Series

url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
page = requests.get(url).text
animals = []

while True:
    #Открываем страницу википедии, нажимаем F12 и мониторим нужный блок
    soup = BeautifulSoup(page, 'lxml')
    names = soup.find('div', class_='mw-category-group').find_all('a')
    for name in names:
        #print(name.text)
        #записываем в список все читаемые данные (!) они записываются в качестве ссылок, не стоит этого забывать
        animals.append(name.text)

    #Заставь программу переходить на следующую страницу
    links = soup.find('div', id='mw-pages').find_all('a')
    for a in links:
        if a.text == 'Следующая страница':
            url = 'https://ru.wikipedia.org/' + a.get('href')
            page = requests.get(url).text
    #Самый простой для меня способ - обозначить последнее наименование на Киррилице это 'Ящурки'
    if 'Ящурки' in animals:
        break

animals_list = list(animals)
s = Series([word[0] for word in animals_list])
letter_count = s.value_counts().sort_index()
print(letter_count)
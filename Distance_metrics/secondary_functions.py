import requests
from bs4 import BeautifulSoup
import pymorphy2
from nltk.corpus import stopwords
import csv


URL = "https://ru.wikipedia.org/wiki/%D0%A4%D1%83%D1%82%D0%B1%D0%BE%D0%BB"



def get_byte(url):
    """mothod to get byte_code"""
    # Извлекаем данные из ссылки
    response = requests.get(url)
    # Переводим содержимое ссылки в байт код
    code = response.content
    return code


def soup_of_code(code):
    """method get html cod"""
    # Достаем html код
    soup = BeautifulSoup(code, 'html.parser')
    return soup


def put_text(soup):
    """put words and count them"""
    # Создается объект класса
    data = {}
    # Достаем текст со страниц вики с тэгами
    text = soup.find('div', class_="mw-parser-output")
    # Проверяем, что на странице есть текст
    if text is None:
        return data
    # Содержимое текста
    text = text.text
    # Преобразовываем текст в список слов
    words = list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), text.split())))
    # Проходимся по всем словам
    for elem in words:
        # Проверяем на наличие слова в мапе
        if elem in data:
            # Если есть, то счетчик увеличиваем
            data[elem] = data[elem] + 1
        else:
            # В противгном случае добавляем со значением один
            data[elem] = 1
    return data


def get_title(url):
    html_text = soup_of_code(get_byte(url))
    title = html_text.findAll("title")[0].text.split("—")[0]
    return title

def delete_stop_words(array_of_words:list):
    stop_words = stopwords.words("russian")
    res = {}
    morph = pymorphy2.MorphAnalyzer()
    for i in array_of_words:
        if i not in stop_words:
            norm_form = morph.parse(i)[0].normal_form
            res[norm_form] = array_of_words[i]
    return res


def get_data_from_csv(file):
    morph = pymorphy2.MorphAnalyzer()
    with open(file, encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        res = set()
        for row in file_reader:
            if row != None:
                for i in row[0].split(' '):
                    res.add(morph.parse(i)[0].normal_form)
    return res



# print(get_data_from_csv("data_of_metrics/наука.csv"))


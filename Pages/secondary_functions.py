import fractions

import requests
from bs4 import BeautifulSoup
from validators import url as valid_url


URL ='https://datalaboratory.one/'


def get_html(url):
    """mothod to get byte_code"""
    # Извлекаем данные из ссылки
    response = requests.get(url)
    # Переводим содержимое ссылки в байт код
    code = BeautifulSoup(response.content, "html.parser")
    return code


def get_urls(soup):
    """get all url"""
    # Поиск по атрибуту и отсеивание лишнего
    new_soup = soup.findAll("a")
    # Проверка на то, что после новый список не пустой
    if len(new_soup) == 0:
        return []
    urls = new_soup[0].findAll("a")
    # Создаем список для вики ссылок
    links = []
    for elem in new_soup:
        # Достаем ссылку без тэгов
        link = str(elem.get("href"))
        # Поверка что сссылка на страницу вики
        if valid_url(link):
            links.append(link)
    return links


def get_title(url):
    html_text = get_html(url)
    title = html_text.findAll("title")[0].text.split("—")[0]
    return title


def make_vector(matrix, vector):
    res = matrix.dot(vector)
    while abs(res[0][0] - vector[0][0]) > fractions.Fraction(1, 1000):
        vector = res
        res = matrix.dot(vector)
    res_vector = []
    for i in vector:
        num, den = str(i[0]).split('/')
        res_vector.append(round(float(num) / float(den), 5))
    return res_vector
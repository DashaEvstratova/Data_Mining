import requests
from bs4 import BeautifulSoup
import pymorphy2
from nltk.corpus import stopwords
import csv
import math


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
    soup = BeautifulSoup(code, "html.parser")
    return soup


def put_text(soup):
    """put words and count them"""
    # Создается объект класса
    data = set()
    # Достаем текст со страниц вики с тэгами
    text = soup.find("div", class_="mw-parser-output")
    # Проверяем, что на странице есть текст
    if text is None:
        return data
    # Содержимое текста
    text = text.text
    # Преобразовываем текст в список слов
    words = list(
        map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), text.split()))
    )
    # Проходимся по всем словам
    for elem in words:
        data.add(elem)
    return data


def get_title(url):
    html_text = soup_of_code(get_byte(url))
    title = html_text.findAll("title")[0].text.split("—")[0]
    return title


def delete_stop_words(array_of_words):
    stop_words = stopwords.words("russian")
    res = set()
    morph = pymorphy2.MorphAnalyzer()
    for i in array_of_words:
        if i not in stop_words and not i.isdigit():
            norm_form = morph.parse(i)[0].normal_form
            res.add(norm_form)
    return res


def get_data_from_csv(file):
    morph = pymorphy2.MorphAnalyzer()
    with open(file, encoding="utf-8") as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        res = []
        for row in file_reader:
            if row != None:
                for i in row[0].split(" "):
                    res.append(morph.parse(i.replace('"', ''))[0].normal_form)
    res = delete_stop_words(res)
    return res


def jaccard(a, b):
    shared = a.intersection(b)
    total = a.union(b)
    res = len(shared) / len(total)
    return res


def result_jaccard(set_of_url, sport, news, shopping, science):
    res_jaccard_science = jaccard(set_of_url, science)
    res_jaccard_sport = jaccard(set_of_url, sport)
    res_jaccard_news = jaccard(set_of_url, news)
    res_jaccard_shopping = jaccard(set_of_url, shopping)
    result_jaccard_number = max(
        res_jaccard_science, res_jaccard_sport, res_jaccard_news, res_jaccard_shopping
    )
    if result_jaccard_number == res_jaccard_science:
        result_jaccard = "Наука"
    elif result_jaccard_number == res_jaccard_sport:
        result_jaccard = "Спорт"
    elif result_jaccard_number == res_jaccard_shopping:
        result_jaccard = "Шопинг"
    else:
        result_jaccard = "Новости"
    return [result_jaccard_number, result_jaccard]


def make_vector(a, all_words):
    a = str(a)[1:-1].replace("'", "").split(",")
    all_words = str(all_words)[1:-1].replace("'", "").split(",")
    first_vector = []
    count = 0
    for i in all_words:
        if i in a:
            first_vector.append("1")
            count += 1
        else:
            first_vector.append("0")
    norm = round(math.sqrt(count), 3)
    result = []
    for i in first_vector:
        if i == "1":
            result.append(round(norm / count, 3))
        else:
            result.append(0)
    return result


def cousins(a, b):
    all_words = a.union(b)
    vec_a = make_vector(a, all_words)
    vec_b = make_vector(b, all_words)
    result = 0
    for i in range(0, len(all_words)):
        result += vec_b[i] * vec_a[i]
    return result


def result_cousins(set_of_url, sport, news, shopping, science):
    res_cousins_science = cousins(set_of_url, science)
    res_cousins_sport = cousins(set_of_url, sport)
    res_cousins_news = cousins(set_of_url, news)
    res_cousins_shopping = cousins(set_of_url, shopping)
    print(res_cousins_science, res_cousins_sport, res_cousins_news, res_cousins_shopping)
    result_cousins_number = max(
        res_cousins_science, res_cousins_sport, res_cousins_news, res_cousins_shopping
    )
    if result_cousins_number == res_cousins_science:
        result_cousins = "Наука"
    elif result_cousins_number == res_cousins_sport:
        result_cousins = "Спорт"
    elif result_cousins_number == res_cousins_shopping:
        result_cousins = "Шопинг"
    else:
        result_cousins = "Новости"
    return [result_cousins_number, result_cousins]


# with open('data_of_metrics/data_of_metrics.txt') as f:
#     scince = set(f.readline().strip().split(':')[1].replace("'", '').split(', '))
#     sport = set(f.readline().strip().split(':')[1].replace("'", '').split(', '))
#     news = set(f.readline().strip().split(':')[1].replace("'", '').split(', '))
#     shoping = set(f.readline().strip().split(':')[1].replace("'", '').split(', '))

# with open('data_of_metrics/data_of_metrics.txt', 'w') as f:
#     f.write(f"наука:{str(get_data_from_csv('data_of_metrics/science.csv'))[1:-1]}")
#     f.write('\n')
#     f.write(f"спорт:{str(get_data_from_csv('data_of_metrics/sport.csv'))[1:-1]}")
#     f.write('\n')
#     f.write(f"шопинг:{str(get_data_from_csv('data_of_metrics/shopping.csv'))[1:-1]}")
#     f.write('\n')
#     f.write(f"новости:{str(get_data_from_csv('data_of_metrics/news.csv'))[1:-1]}")
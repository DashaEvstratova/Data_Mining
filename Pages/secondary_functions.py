import requests
from bs4 import BeautifulSoup
from validators import url as valid_url


WIKI_DOMAIN = "https://ru.wikipedia.org"


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
    new_soup = soup.select("div[class=mw-parser-output]")
    # Проверка на то, что после новый список не пустой
    if len(new_soup) == 0:
        return []
    urls = new_soup[0].findAll("a")
    # Создаем список для вики ссылок
    links = []
    for elem in urls:
        # Достаем ссылку без тэгов
        link = str(elem.get("href"))
        # Поверка что сссылка на страницу вики
        if "/wiki/" in link:
            url = "".join([WIKI_DOMAIN, link])
            if valid_url(url):
                links.append(url)
    return links


def get_title(url):
    html_text = get_html(url)
    title = html_text.findAll("title")[0].text.split("—")[0]
    return title

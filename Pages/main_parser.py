from concurrent.futures import ThreadPoolExecutor

from Pages.secondary_functions import get_html, get_urls

URL = "https://ru.wikipedia.org/wiki/Special:Random"


def wiki_parser(url: str):
    """method from url to file"""
    # Массив с ссылками
    working_path = []
    working_path.append("1")
    working_path.append(url)
    working_path.append("1")
    working_path += get_urls(get_html(url))
    return working_path


def parse_depth(url: str, depth=3):
    """method parse_depth"""
    # Делаем из списка множество ссылок, чтоб убрать дубликаты
    urls = wiki_parser(url)
    urls = urls[3:]
    urls.append(url)
    result = dict()
    result[url] = urls
    next_step = []
    urls = set(urls)
    # Цикл для счета потоков
    for _ in range(depth - 1):
        with ThreadPoolExecutor(4) as thread:
            new_urls = thread.map(wiki_parser, urls)
            for new_url in new_urls:
                if len(new_url) != 3:
                    links = new_url[3:]
                    result[new_url[1]] = links
                    next_step += links
            urls = set(next_step) - urls
    return result

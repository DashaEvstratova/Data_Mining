import numpy as np
import fractions
from Pages.models import List_of_urls, Result_url


def make_main_url(f_u):
    class_main_url = Result_url.objects.filter(first_url=f_u)
    main_url = []
    for i in class_main_url:
        if i.number_of_link != 0:
            main_url.append(i.child_link)
    len_of_url = len(main_url)
    res_len = 0
    while res_len != len_of_url:
        for i in main_url:
            const = 0
            object_id = Result_url.objects.get(first_url=f_u, child_link=i).id
            list_url = List_of_urls.objects.filter(first_url=f_u, main_url=object_id)
            for j in list_url:
                if j.child_link in main_url:
                    const = 1
                    break
            if const == 0:
                main_url.remove(i)
        res_len = len_of_url
        len_of_url = len(main_url)
    return main_url


def make_main_id(f_u):
    main_url = make_main_url(f_u)
    main_id = []
    class_main_url = []
    for i in main_url:
        url = Result_url.objects.get(first_url=f_u, child_link=i)
        class_main_url.append(url)
    for i in class_main_url:
        url = i.child_link
        if List_of_urls.objects.filter(child_link=url, first_url=f_u).exists():
            main_id.append(i.id)
    return main_id


def make_matrix(f_u, main_id):
    matrix = []
    for i in main_id:
        line = []
        url_i = Result_url.objects.get(id=i, first_url=f_u).child_link
        for j in main_id:
            if i == j:
                line.append(0)
            else:
                count_url = Result_url.objects.get(id=j, first_url=f_u).number_of_link
                list_i = List_of_urls.objects.filter(main_url=j, first_url=f_u)
                list_url = []
                for q in list_i:
                    list_url.append(q.child_link)
                if url_i in list_url:
                    probability = fractions.Fraction(1, count_url)
                    line.append(probability)
                else:
                    line.append(0)
        matrix.append(line)
    return matrix


def make_first_vector(main_id):
    vector = []
    for i in main_id:
        vector.append([fractions.Fraction(1, len(main_id))])
    return vector


def from_factory_to_float(number):
    num, den = str(number).split("/")
    res = round(float(num) / float(den), 10)
    return res


def make_vector(matrix, vector):
    res = matrix.dot(vector)
    while abs(res[0][0] - vector[0][0]) > fractions.Fraction(1, 1000):
        vector = res
        res = matrix.dot(vector)
    res_vector = []
    for i in vector:
        res_vector.append(from_factory_to_float(i[0]))
    return res_vector


def count_other_links(link, f_u):
    main_urls = List_of_urls.objects.filter(child_link=link)
    probability = 0
    for i in main_urls:
        main_url = i.main_url
        res = round(1 / main_url.number_of_link, 10)
        probability += main_url.link_probability * res
    main = Result_url.objects.get(child_link=link, first_url=f_u)
    main.link_probability = round(probability, 10)
    main.save()
    return True


def make_from_class_to_url(class_of_url):
    urls = []
    for i in class_of_url:
        urls.append(i.child_link)
    return urls


def check_url(f_u, link, main_list_url):
    list_id_main = List_of_urls.objects.filter(child_link=link)
    count = 0
    for i in list_id_main:
        main_url = i.main_url.child_link
        if main_url in main_list_url:
            count += 1
    if count == len(list_id_main):
        count_other_links(link, f_u)
        return True
    return False


def get_probability(first_url):
    f_u = first_url.id
    main_id = make_main_id(f_u)
    matrix = make_matrix(f_u, main_id)
    vector = make_first_vector(main_id)
    matrix = np.array(matrix)
    vector = np.array(vector)
    res_vector = make_vector(matrix, vector)
    count = 0
    for i in main_id:
        main = Result_url.objects.get(id=i, first_url=f_u)
        main.link_probability = res_vector[count]
        count += 1
        main.save()
    all_url = make_from_class_to_url(Result_url.objects.filter(first_url=f_u))
    main_list_url = make_from_class_to_url(
        Result_url.objects.exclude(link_probability=None)
    )
    while len(all_url) != 0:
        for i in all_url:
            if check_url(f_u, i, main_list_url):
                main_list_url.append(i)
                all_url.remove(i)

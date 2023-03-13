import numpy as np
import fractions
from django.shortcuts import render
from django.views import View
from django.db import IntegrityError
from Pages.forms import FirstUrlForm
from Pages.main_parser import parse_depth
from Pages.models import First_urls, List_of_urls, Result_url, Matrix_url
from Pages.secondary_functions import get_title, make_vector


class MainView(View):
    def _render(self, request, form=None, message=None):
        list = First_urls.objects.all()
        return render(
            request,
            "Pages/main.html",
            {"form": form or FirstUrlForm(), "message": message, "list": list},
        )

    def get(self, request, *args, **kwargs):
        return self._render(request, None, None)

    def post(self, request, *args, **kwargs):
        form = FirstUrlForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data["url"]
                title = get_title(url)
                First_urls.objects.create(url=url, title=title)
                result = parse_depth(url, 2)
                first_url = First_urls.objects.get(url=url)
                for i in result:
                    Result_url.objects.create(first_url=first_url,
                                              child_link=i,
                                              number_of_link=len(result[i]))
                    main_url = Result_url.objects.get(child_link=i)
                    for j in result[i]:
                        List_of_urls.objects.create(
                            first_url=first_url, main_url=main_url, child_link=j
                        )
                return self._render(request, form)
            except IntegrityError:
                message = "Эта ссылка уже была обработана"
                return self._render(request.path, form, message)
        else:
            return self._render(request, form)


def get_probability(first_url):
    f_u = first_url.id
    class_main_url = Result_url.objects.filter(first_url=f_u)
    main_id = []
    main_url = []
    # достаем ссылки, которые на что-то указывают
    for i in class_main_url:
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
    class_main_url = []
    for i in main_url:
        url = Result_url.objects.get(first_url=f_u, child_link=i)
        class_main_url.append(url)
    for i in class_main_url:
        url = i.child_link
        if List_of_urls.objects.filter(child_link=url, first_url=f_u).exists():
            main_id.append(i.id)
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
    vector = []
    for i in main_id:
        vector.append([fractions.Fraction(1, len(main_id))])
    Matrix_url.objects.create(first_url=first_url,
                              matrix=matrix,
                              vector=vector)
    matrix = np.array(matrix)
    vector = np.array(vector)
    res_vector = make_vector(matrix, vector)
    count = 0
    for i in main_id:
        main = Result_url.objects.get(id=i, first_url=f_u)
        main.link_probability = res_vector[count]
        count += 1
        main.save()



def list_url(request, title):
    first_url = First_urls.objects.get(title=title)
    f_u = first_url.id
    if Result_url.objects.filter(first_url=f_u)[0].link_probability is None:
        get_probability(first_url)

    return render(request,
        "Pages/link_page.html")

from django.shortcuts import render
from django.views import View
from django.db import IntegrityError
from Pages.forms import FirstUrlForm
from Pages.main_parser import parse_depth
from Pages.models import First_urls, List_of_urls, Result_url
from Pages.secondary_functions import get_title
from Pages.count_probability import get_probability


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
                    if Result_url.objects.filter(child_link=i).exists():
                        url = Result_url.objects.get(child_link=i)
                        url.number_of_link = len(result[i])
                        url.save()
                    else:
                        Result_url.objects.create(
                            first_url=first_url,
                            child_link=i,
                            number_of_link=len(result[i]),
                        )
                    main_url = Result_url.objects.get(child_link=i)
                    for j in result[i]:
                        List_of_urls.objects.create(
                            first_url=first_url, main_url=main_url, child_link=j
                        )
                        if not Result_url.objects.filter(child_link=j).exists():
                            Result_url.objects.create(
                                first_url=first_url, child_link=j, number_of_link=0
                            )
                return self._render(request, form)
            except IntegrityError:
                message = "Эта ссылка уже была обработана"
                return self._render(request.path, form, message)
        else:
            return self._render(request, form)


def list_url(request, title):
    first_url = First_urls.objects.get(title=title)
    f_u = first_url.id
    list_of_link = Result_url.objects.filter(first_url=f_u)
    if list_of_link[0].link_probability is None:
        get_probability(first_url)
        lists = List_of_urls.objects.filter(first_url=f_u)
        with open('/home/daria/PycharmProjects/Page_Rank/data.txt', 'w') as f:
            for i in lists:
                main_id = i.main_url.id
                child_id = Result_url.objects.get(child_link=i.child_link, first_url=f_u).id
                f.write(f'{main_id}, {child_id}')
                f.write('\n')
    list_of_link = list_of_link.order_by("-link_probability")
    return render(request, "Pages/link_page.html", {"list_url": list_of_link,
                                                    "first_url": first_url})

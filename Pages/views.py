from django.shortcuts import render
from django.views import View
from django.db import IntegrityError
from Pages.forms import FirstUrlForm
from Pages.main_parser import parse_depth
from Pages.models import First_urls, List_of_urls, Result_url
from Pages.secondary_functions import get_title


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
                main_url = First_urls.objects.get(url=url)
                for i in result:
                    for j in result[i]:
                        List_of_urls.objects.create(
                            first_url=main_url, main_url=i, child_link=j
                        )
                    Result_url.objects.create(first_url=main_url,
                                              child_link= i,
                                              number_of_link= len(result[i]))
                return self._render(request, form)
            except IntegrityError:
                message = "Эта ссылка уже была обработана"
                return self._render(request.path, form, message)
        else:
            return self._render(request, form)

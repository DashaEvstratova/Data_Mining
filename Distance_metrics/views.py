from django.shortcuts import render
from django.views import View
from django.db import IntegrityError

from Distance_metrics.forms import UrlForm
from Distance_metrics.models import Url, Result
from Distance_metrics.secondary_functions import (
    get_title,
    delete_stop_words,
    put_text,
    soup_of_code,
    get_byte,
    result_jaccard,
    result_cousins,
)


class MainView(View):
    def _render(self, request, form=None, message=None):
        list = Result.objects.all()
        return render(
            request,
            "Distance_metrics/main.html",
            {"form": form or UrlForm(), "message": message, "list": list},
        )

    def get(self, request, *args, **kwargs):
        return self._render(request, None, None)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if form.is_valid():
            try:
                url = form.cleaned_data["url"]
                title = get_title(url)
                Url.objects.create(url=url, title=title)
                data_of_url = Url.objects.get(url=url)
                set_of_url = delete_stop_words(put_text(soup_of_code(get_byte(url))))
                with open("Distance_metrics/data_of_metrics/data_of_metrics.txt") as f:
                    science = set(
                        f.readline().strip().split(":")[1].replace("'", "").split(", ")
                    )
                    sport = set(
                        f.readline().strip().split(":")[1].replace("'", "").split(", ")
                    )
                    news = set(
                        f.readline().strip().split(":")[1].replace("'", "").split(", ")
                    )
                    shopping = set(
                        f.readline().strip().split(":")[1].replace("'", "").split(", ")
                    )
                result_of_jaccard_number = result_jaccard(
                    set_of_url, sport, news, shopping, science
                )[0]
                result_of_jaccard = result_jaccard(
                    set_of_url, sport, news, shopping, science
                )[1]
                result_of_cousins_number = result_cousins(
                    set_of_url, sport, news, shopping, science
                )[0]
                result_of_cousins = result_cousins(
                    set_of_url, sport, news, shopping, science
                )[1]
                Result.objects.create(url=data_of_url,
                                      category_jaccard=result_of_jaccard,
                                      category_jaccard_number=result_of_jaccard_number,
                                      category_cosinus=result_of_cousins,
                                      category_cosinus_number=result_of_cousins_number)
                return self._render(request, form)
            except IntegrityError:
                message = "Эта ссылка уже была обработана"
                return self._render(request.path, form, message)
        else:
            return self._render(request, form)

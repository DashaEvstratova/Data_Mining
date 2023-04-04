from django.shortcuts import render
from django.views import View

from Distance_metrics.forms import UrlForm
from Distance_metrics.models import Url


class MainView(View):
    def _render(self, request, form=None, message=None):
        list = Url.objects.all()
        return render(
            request,
            "Distance_metrics/main.html",
            {"form": form or UrlForm(), "message": message, "list": list},
        )

    def get(self, request, *args, **kwargs):
        arr = set()
        with open('sport.txt') as f:
            n = f.readline().strip().split(' ')
            while n[0] != '0':
                for i in n:
                    arr.add(i)
                n = f.readline().strip().split(' ')
                n = f.readline().strip().split(' ')
        return self._render(request, None, None)

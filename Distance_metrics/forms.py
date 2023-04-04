from django import forms

from Pages.models import First_urls


class UrlForm(forms.ModelForm):
    class Meta:
        model = First_urls
        fields = ["url"]
        labels = {"url": "Ссылка для анализа "}

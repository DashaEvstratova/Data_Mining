from django.db import models


class Url(models.Model):
    url = models.CharField(unique=True, max_length=1000)
    title = models.CharField(max_length=225)


class Result(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    category_jaccard = models.CharField(max_length=1000)
    category_jaccard_number = models.FloatField()
    category_cosinus = models.CharField(max_length=1000)
    category_cosinus_number = models.FloatField()

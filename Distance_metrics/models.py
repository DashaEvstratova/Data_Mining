from django.db import models

class Url(models.Model):
    url = models.CharField(unique=True, max_length=1000)
    title = models.CharField(max_length=225)


class Result(models.Model):
    first_url = models.ForeignKey(Url, on_delete=models.CASCADE)
    category = models.CharField(max_length=1000)


class List_of_words(models.Model):
    first_url = models.ForeignKey(Url, on_delete=models.CASCADE)
    word = models.CharField(max_length=1000)

class List_of_semantic_words(models.Model):
    category = models.CharField(max_length=1000)
    word = models.CharField(max_length=1000)
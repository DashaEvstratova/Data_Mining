from django.db import models


class First_urls(models.Model):
    url = models.CharField(unique=True, max_length=1000)
    title = models.CharField(max_length=225)


class Result_url(models.Model):
    first_url = models.ForeignKey(First_urls, on_delete=models.CASCADE)
    child_link = models.CharField(max_length=1000, unique=True)
    number_of_link = models.IntegerField()
    link_probability = models.FloatField(null=True)


class List_of_urls(models.Model):
    first_url = models.ForeignKey(First_urls, on_delete=models.CASCADE)
    main_url = models.ForeignKey(Result_url, on_delete=models.CASCADE)
    child_link = models.CharField(max_length=1000)

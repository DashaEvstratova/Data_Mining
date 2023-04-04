# Generated by Django 4.1.7 on 2023-04-04 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Url",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.CharField(max_length=1000, unique=True)),
                ("title", models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(max_length=1000)),
                (
                    "first_url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Distance_metrics.url",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="List_of_words",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("word", models.CharField(max_length=1000)),
                (
                    "first_url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Distance_metrics.url",
                    ),
                ),
            ],
        ),
    ]

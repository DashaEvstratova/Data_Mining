# Generated by Django 4.1.7 on 2023-04-04 16:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Distance_metrics", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="List_of_semantic_words",
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
                ("word", models.CharField(max_length=1000)),
            ],
        ),
    ]
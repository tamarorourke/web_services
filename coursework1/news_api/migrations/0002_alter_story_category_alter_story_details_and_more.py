# Generated by Django 4.2.11 on 2024-03-22 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="story",
            name="category",
            field=models.CharField(
                choices=[
                    ("pol", "Politics"),
                    ("art", "Art"),
                    ("tech", "Technology"),
                    ("trivia", "Trivia"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="story", name="details", field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name="story", name="headline", field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="story",
            name="region",
            field=models.CharField(
                choices=[
                    ("uk", "United Kingdom"),
                    ("eu", "European Union"),
                    ("w", "World"),
                ],
                max_length=50,
            ),
        ),
    ]

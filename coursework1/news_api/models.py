from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

class Story(models.Model):
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]
    REGION_CHOICES = [
        ('uk', 'United Kingdom'),
        ('eu', 'European Union'),
        ('w', 'World'),
    ]

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=128)


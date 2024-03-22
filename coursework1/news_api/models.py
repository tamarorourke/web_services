from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

class Story(models.Model):
    headline = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    region = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=150)


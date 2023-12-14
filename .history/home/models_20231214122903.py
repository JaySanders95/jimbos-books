from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.Datefield(null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.Charfield(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.Charfield(max_length=100)
    author = models.ForeignKey(Author, on_delete.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre)
    publication_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
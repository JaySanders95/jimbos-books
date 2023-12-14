from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Customer(models.Model):
    user = models.OnetoOneField(User, on_delete=models.CASCADE)
    name = models.Charfield(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15)

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
    genre = models.ForeignKey(Genre, on_delete.SET_NULL, null=True)
    publication_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField

    def __str__(self):
        return self.title
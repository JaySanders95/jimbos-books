from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Author*(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.Datefield(null=True, blank=True)
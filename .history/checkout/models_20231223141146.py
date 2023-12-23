from django.db import models

# Create your models here.

class Order(models.Model):
    order_number = models.Charfield(max_length=32, null=False)
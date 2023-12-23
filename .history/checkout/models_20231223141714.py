from django.db import models

# Create your models here.

class Order(models.Model):
    order_number = models.Charfield(max_length=32, null=False, editable=False)
    full_name = models.Charfield(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=)
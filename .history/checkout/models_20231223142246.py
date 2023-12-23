from django.db import models

# Create your models here.

class Order(models.Model):
    order_number = models.Charfield(max_length=32, null=False, editable=False)
    full_name = models.Charfield(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    country = models.Charfield(max_length=40, null=False, blank=False)
    phone_number = models.Charfield(max_length=15, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.Charfield(max_length=40, null=False, blank=False)
    street_address1 = models.Charfield(max_length=80, null=False, blank=False)
    
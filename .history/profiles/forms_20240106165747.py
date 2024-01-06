# forms.py

from django import forms
from django_countries.fields import CountryField
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    country = CountryField().formfield()

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'country', 'phone_number', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county', 'additional_field1', 'additional_field2']

    
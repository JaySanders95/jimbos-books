from django import forms
from .models import Order
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class OrderForm(forms.ModelForm):
    country = CountryField().formField

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 
                    'street_address1', 'street_address2', 
                    'town_or_city','postcode','country',
                    'county')
        
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'phone_number': 'Phone Number',
                'country': 'Country',
                'postcode': 'Postal Code',
                'town_or_city': 'Town or City',
                'street_address1': 'Street Address 1',
                'street_address2': 'Street Address 2',
                'county': 'County',
            }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False    
        
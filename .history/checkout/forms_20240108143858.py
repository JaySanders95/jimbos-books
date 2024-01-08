from django import forms
from .models import Order
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class OrderForm(forms.ModelForm):
    country = CountryField().formfield()

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

        # Add Crispy-forms setup for the new country field
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('full_name', css_class='stripe-style-input'),
            Field('email', css_class='stripe-style-input'),
            Field('phone_number', css_class='stripe-style-input'),
            Field('country', css_class='custom-dropdown-class'),
            Field('postcode', css_class='stripe-style-input'),
            Field('town_or_city', css_class='stripe-style-input'),
            Field('street_address1', css_class='stripe-style-input'),
            Field('street_address2', css_class='stripe-style-input'),
            Field('county', css_class='stripe-style-input'),
        )
        def clean_phone_number(self):
        return self.clean_generic_field('phone_number', r'^[0-9+]*$', "Phone number can only contain digits and '+' sign.")

    def clean_postcode(self):
        return self.clean_generic_field('postcode', r'^[0-9A-Za-z\s]*$', "Postcode can only contain alphanumeric characters and spaces.")

    def clean_town_or_city(self):
        return self.clean_generic_field('town_or_city', r'^[0-9A-Za-z\s]*$', "Town or city can only contain alphanumeric characters and spaces.")

    def clean_street_address1(self):
        return self.clean_generic_field('street_address1', r'^[0-9A-Za-z\s]*$', "Street Address 1 can only contain alphanumeric characters and spaces.")

    def clean_street_address2(self):
        return self.clean_generic_field('street_address2', r'^[0-9A-Za-z\s]*$', "Street Address 2 can only contain alphanumeric characters and spaces.")

    def clean_county(self):
        return self.clean_generic_field('county', r'^[0-9A-Za-z\s]*$', "County can only contain alphanumeric characters and spaces.")

    def clean_generic_field(self, field_name, regex_pattern, error_message):
        field_value = self.cleaned_data.get(field_name)
        # Check if the field contains special characters
        if not re.match(regex_pattern, field_value):
            raise ValidationError(error_message)
        return field_value
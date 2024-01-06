from django import forms
from django_countries.fields import CountryField
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    country = CountryField().formfield()

    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'country', 'phone_number', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county']

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Set initial values for fields based on the instance data
        if self.instance:
            self.fields['full_name'].initial = self.instance.full_name
            self.fields['email'].initial = self.instance.email
            self.fields['country'].initial = self.instance.country
            self.fields['phone_number'].initial = self.instance.phone_number
            self.fields['postcode'].initial = self.instance.postcode
            self.fields['town_or_city'].initial = self.instance.town_or_city
            self.fields['street_address1'].initial = self.instance.street_address1
            self.fields['street_address2'].initial = self.instance.street_address2
            self.fields['county'].initial = self.instance.county

        # Provide an empty option for the country field
        self.fields['country'].empty_label = 'Select your country'
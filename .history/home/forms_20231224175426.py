from django import forms
from .models import Reviews


class ReviewsForm(forms.Form):
    class Meta:
        model = Reviews
        fields = 
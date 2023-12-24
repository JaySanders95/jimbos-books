from django import forms
from .models import Reviews


class ReviewsForm(forms.Form):
    class Meta:
        model = Reviews
        fields = ['full-name', 'review_title',
                    'review_body', 'review_image', 
                    'rating']
    def clean_rating(self):
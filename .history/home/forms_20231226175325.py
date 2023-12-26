from django import forms
from .models import Reviews
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['full_name', 'review_title', 'review_body', 'review_image', 'rating']

    def __init__(self, *args, **kwargs):
        super(ReviewsForm, self).__init__(*args, **kwargs)
        
        # Crispy Forms helper configuration
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Submit Review'))

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0 and 5.")
        return rating


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


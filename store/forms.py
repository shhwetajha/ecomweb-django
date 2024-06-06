from django import forms
from .models import *

class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject','review','rating']
        
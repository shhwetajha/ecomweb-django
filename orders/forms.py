from django import forms
from .models import *
class OrderForms(forms.ModelForm):
    class Meta:
        model=order
        fields=['first_name','last_name','email','phone','address_line_1','address_line_2','state','city','country','order_note']


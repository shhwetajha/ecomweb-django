from orders.models import *
from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2',
                'country','city','state','order_note']



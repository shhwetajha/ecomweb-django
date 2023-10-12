from django.urls import path
from orders.views import *


urlpatterns=[

path('place_order/',place_order,name='placeorder'),
path('payment/',view_payment,name='payment'),
path('order_complete/',Order_Complete,name='order_complete')

]
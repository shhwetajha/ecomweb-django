from django.urls import path
from.views import *
urlpatterns=[
    path('order_det/',view_order,name='order'),
    path('payment/',payment,name='payment'),
    path('order_complete/',order_complete,name='order_complete')
]
from django.urls import path
from  .views import *

urlpatterns=[
    path("",view_cart,name='cart'),
    path('add_to_cart/<int:product_id>/',add_cart,name='add_to_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',remove_cart_item,name='remove_cart_item')
]
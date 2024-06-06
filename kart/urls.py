from django.urls import path
from .views import *

urlpatterns=[
    path('addkart/<int:product_id>/',add_kart,name='add_to_kart'),
    path('cart/',cart_details,name='cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',remove_cart_item,name='remove_item'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',remove_cart,name='remove_cart'),
    path('checkout/',view_checkout,name='checkout'),
]

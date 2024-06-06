from django.urls import path
from .views import *

urlpatterns=[
    path('',view_store,name='store'),
    path('category/<slug:category_slug>/',view_store,name='categories_det'),
    path('category/product_det/<slug:category_slug>/<slug:slug>/',product_detail,name='product_det'),
    path('search/',search,name='search'),
    path('review_rating/<int:productid>/',review_rating,name='reviewrating')
]
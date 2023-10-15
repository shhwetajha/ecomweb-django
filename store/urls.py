from django.urls import path
from .views import *

urlpatterns=[
    path('',view_store,name='store'),
    path('category/<slug:category_slug>/',view_store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',product_detail,name='product_detail'),
    path('search/',search,name='search'),
    path('rating_review/<int:product_id>/',rating_review,name='reviewrating'),
   
] 
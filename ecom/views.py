from django.shortcuts import render,redirect
from django.http import HttpResponse
from store.models import *


def view_home(request):
    productss=products.objects.all().filter(is_available=True)

    for product in productss:
            review=ReviewRating.objects.filter(product_id=product.id,status=True)
    context={'products':productss,'review':review}
    return render(request,'home.html',context)


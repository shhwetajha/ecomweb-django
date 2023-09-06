from django.shortcuts import render,get_object_or_404
from .models import *
from ecomapp.models import *

# Create your views here.

def view_store(request,category_slug=None):
    categories=None
    productss=None

    if category_slug != None:
        # get_object_or_404-it will just bring in the cat if found
        categories=get_object_or_404(Category,slug=category_slug)
        # it wll bring all the products that is of above particular category
        productss=products.objects.filter(category=categories,is_available=True)
        product_count=productss.count()
    else:   
        productss=products.objects.all().filter(is_available=True)
        product_count=productss.count()
    context={'products':productss,'product_count':product_count}
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product=products.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context={'single_product':single_product}
    return render(request,'store/product_det.html',context)
    



from django.shortcuts import render,redirect
from django.http import HttpResponse
from store.models import *


def view_home(request):
    productss=products.objects.all().filter(is_available=True)
    context={'products':productss}
    return render(request,'home.html',context)



from django.shortcuts import render,get_object_or_404
from .models import *
from ecomapp.models import *
from cartt.models import *
from cartt.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

def view_store(request,category_slug=None):
    categories=None
    productss=None
 
    if category_slug != None:
        # get_object_or_404-it will just bring in the cat if found
        categories=get_object_or_404(Category,slug=category_slug)
        # it wll bring all the products that is of above particular category
        productss=products.objects.filter(category=categories,is_available=True)
        paginator =Paginator(productss,2)
        paged=request.GET.get('page')
        paged_products=paginator.get_page(paged)
        total_page=paged_products.paginator.num_pages
        total_page_list=[n+1 for n in range(total_page)]
        product_count=productss.count()
    else:   
        productss=products.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(productss,2)
        paged=request.GET.get('page')
        paged_products=paginator.get_page(paged)
        total_page=paged_products.paginator.num_pages
        product_count=productss.count()
        
    context={'products':paged_products,'product_count':product_count,'last':total_page,'total_page_list':[n+1 for n in range (total_page)]}

    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product=products.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context={'single_product':single_product,'in_cart':in_cart}
    return render(request,'store/product_det.html',context)
    
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
       
        if keyword:
            Product=products.objects.order_by('created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count=Product.count()
    context={'products':Product,'product_count':product_count,}
    return render(request,'store/store.html',context)   


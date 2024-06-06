from django.shortcuts import render,redirect
from great.models import *
from .models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import *



# Create your view
def view_store(request,category_slug=None):
    products=None
    if category_slug!=None:
        category=get_object_or_404(categories,slug=category_slug)
        products=Products.objects.filter(categories=category,is_available=True).order_by('id')
        paginator=Paginator(products,2)
        page_number=request.GET.get('page') 
        paged_obj=paginator.get_page(page_number)
        last_page=paged_obj.paginator.num_pages
        product_count=products.count()     
    else:
        products=Products.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,2)
        page_number=request.GET.get('page')
        paged_obj=paginator.get_page(page_number)
        last_page=paged_obj.paginator.num_pages
        product_count=products.count()
    context={'products':products,'product_count':product_count,'page_list':[n+1 for n in range (last_page)],'last_page':last_page,'products':paged_obj}
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,slug):
    single_product=Products.objects.get(categories__slug=category_slug,slug=slug)
    if request.user.is_authenticated:
        try:
            orderProduct=orderdetail.objects.filter(user=request.user,product_id=single_product.id).exists()
        except orderdetail.DoesNotExist:
            orderProduct=None
    else:
        orderProduct=None

    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)
    product_gallery=ProductGallery.objects.filter(product_id=single_product.id)
    context={'single_product':single_product,'product_gallery':product_gallery,'orderproduct':orderProduct,'review':reviews}
    return render(request,'store/product_det.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']

        if keyword:
            products=Products.objects.order_by('created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count=products.count()
    context={'products':products,'product_count':product_count,}
    return render(request,'store/store.html',context)

@login_required(login_url='login')
def review_rating(request,productid):
    url=request.META.get('HTTP_REFERER')
    print(url)
    # product=Products.objects.get(id=productid)
    try:
        review=ReviewRating.objects.get(user=request.user,product_id=productid)
        if request.method=='POST':
            forms=ReviewRatingForm(request.POST,instance=review)
            if forms.is_valid():
                forms.save()
                messages.success(request,"review has been successfully updated!")
                return redirect(url)
    except ReviewRating.DoesNotExist:
        forms=ReviewRatingForm(request.POST)
        if forms.is_valid():
            data=ReviewRating()
            data.user=request.user
            data.product_id=productid
            data.subject=forms.cleaned_data['subject']
            data.review=forms.cleaned_data['review']
            data.rating=forms.cleaned_data['rating']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,'review has been successfully saved!')
            return redirect(url)

    



    
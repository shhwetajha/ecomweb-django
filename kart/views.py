from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from store.models import *
from.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
def _kart_id(request):
    kart=request.session.session_key
    if not kart:
        kart=request.session.create()
    return kart

def add_kart(request,product_id):
    current_user=request.user
    products=Products.objects.get(id=product_id)


    if current_user.is_authenticated:
        product_variation=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                print(key)
                value=request.POST[key]
                print(value)
                try:
                    Variation=variations.objects.get(product=products,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(Variation)
                    print(product_variation)
                except Exception as e:
                    print(e)              
        
        cart_item_exist=Kart_item.objects.filter(user=current_user,product=products).exists()
        print("True")
        if cart_item_exist:
            cart_item=Kart_item.objects.filter(user=current_user,product=products)
            ex_variations=[]
            ex_var_id=[]
            for item in cart_item:
                variation=item.variations.all()
                ex_variations.append(list(variation))
                ex_var_id.append(item.id)
            print(ex_variations)
            print(product_variation)

            if product_variation in ex_variations:
                Index=ex_variations.index(product_variation)
                item_id=ex_var_id[Index]
                item=Kart_item.objects.get(product=products,id=item_id)
                item.quantity+=1
                item.save()
                print('Yes')
            else:
                item=Kart_item.objects.create(product=products,user=current_user,quantity=1)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=Kart_item.objects.create(product=products,user=current_user,quantity=1)
            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                try:
                    Variation=variations.objects.get(product=products,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(Variation)
                except:
                    pass
        try:
            cart=Kart.objects.get(kart_id=_kart_id(request))
        except Kart.DoesNotExist:
            cart=Kart.objects.create(kart_id=_kart_id(request))
        cart.save()

        Iscartitemexist=Kart_item.objects.filter(cart=cart,product=products).exists()
        if Iscartitemexist:
            cartitem=Kart_item.objects.filter(cart=cart,product=products)
            ex_variation=[]
            ex_id=[]
            for item in cartitem:
                variationss=item.variations.all()
                ex_variation.append(list(variationss))
                ex_id.append(item.id)

            if product_variation in ex_variation:
                Index=ex_variation.index(product_variation)
                item_id=ex_id[Index]
                items=Kart_item.objects.get(product=products,id=item_id)
                items.quantity+=1
                items.save()

            else:
                cart_item=Kart_item.objects.create(product=products,cart=cart,quantity=1)
                if len(product_variation)>0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                cart_item.save()
        else:
            cart_item=Kart_item.objects.create(product=products,cart=cart,quantity=1)
            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
 

def cart_details(request,total=0,cart_item=None):
    try:
        grand_total=0
        tax=0
        quantity=0
        current_user=request.user
        if current_user.is_authenticated:
            cart_item=Kart_item.objects.filter(user=current_user,is_active=True)
        else:
            cart=Kart.objects.get(kart_id=_kart_id(request))
            cart_item=Kart_item.objects.filter(cart=cart)
        for item in cart_item:
            total+=item.product.price*item.quantity
            quantity+=item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={'cart_items':cart_item,'total':total,'grand_total':grand_total,'tax':tax,'quantity':quantity}
    return render(request,'store/cart.html',context)


def remove_cart_item(request,product_id,cart_item_id):
    products=get_object_or_404(Products,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=Kart_item.objects.get(product=products,user=request.user,id=cart_item_id)
        else:
            cart=Kart.objects.get(kart_id=_kart_id(request))
            cart_item=Kart_item.objects.get(cart=cart,product=products,id=cart_item_id)
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    products=get_object_or_404(Products,id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item=Kart_item.objects.get(user=request.user,product=products,id=cart_item_id)
        else:
            cart=Kart.objects.get(kart_id=_kart_id(request))
            cart_item=Kart_item.objects.get(cart=cart,product=products,id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

@login_required(login_url='login')
def view_checkout(request,quantity=0,cart_items=None):  
    try:
        total=0
        grand_total=0
        tax=0
        if request.user.is_authenticated:
            cart_items=Kart_item.objects.filter(user=request.user,is_active=True)
        else:
            cart=Kart.objects.get(kart_id=_kart_id(request))
            cart_items=Kart_item.objects.filter(cart=cart)

        for item in cart_items:
            total+=item.product.price*item.quantity
            quantity+=item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={'cart_items':cart_items,'total':total,'quantity':quantity,'tax':tax,'grand_total':grand_total}
    return render(request,'store/checkout.html',context)
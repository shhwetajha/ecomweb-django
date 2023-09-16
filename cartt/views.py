from django.shortcuts import render,redirect,get_object_or_404
from store.models import products
from .models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import *

# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
    

def add_cart(request,product_id):
    Product=products.objects.get(id=product_id)
    product_variation=[]
    if request.method=='POST':
        for i in request.POST:
            key=i
            value=request.POST[key]
            try:
                variation=Variation.objects.get(Products=Product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
        
    
        try:
            Cart=cart.objects.get(cart_id=_cart_id(request))
        except cart.DoesNotExist:
            Cart=cart.objects.create(cart_id=_cart_id(request))
        Cart.save()



        cart_Item_exist=CartItem.objects.filter(product=Product,cart=Cart).exists()
        if cart_Item_exist:
                cart_Item=CartItem.objects.filter(product=Product,cart=Cart)
                ex_var_list=[]
                var_id=[]
                for item in cart_Item:
                    existing_variations=item.variation.all()
                    ex_var_list.append(list(existing_variations))
                    var_id.append(item.id)


                if product_variation in ex_var_list:
                    Index=ex_var_list.index(product_variation)
                    item_id=var_id[Index]
                    print(item_id)
                    item=CartItem.objects.get(product=Product,id=item_id)
                    item.quantity+=1
                    item.save()
                else:
                    item=CartItem.objects.create(product=Product,cart=Cart,quantity=1)
                    if len(product_variation)>0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                    item.save()

        else:
            Cartitem=CartItem.objects.create(product=Product,cart=Cart,quantity=1)
            if len(product_variation)>0: 
                Cartitem.variation.clear()
                Cartitem.variation.add(*product_variation)
            Cartitem.save()
        return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    Cart=cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(products,id=product_id)
    cart_item=CartItem.objects.get(cart=Cart,product=product,id=cart_item_id)
    try:

        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

   
def remove_cart_item(request,product_id,cart_item_id):
    Cart=cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(products,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=Cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart') 


def view_cart(request,total=0,quantity=0,cart_item=None):
    try:
        Cart=cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=Cart,is_active=True)
        for cart_item in cart_items:
            total+=cart_item.product.price*cart_item.quantity
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={'total':total,'quantity':quantity,'cart_items':cart_items,'tax':tax,'grand_total':grand_total}
    return render(request,'store/cart.html',context)

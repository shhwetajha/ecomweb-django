from django.shortcuts import render,redirect
from cartt.models import *
from orders.forms import OrderForm
from orders.models import *
from django.http import HttpResponse,JsonResponse
import datetime
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
def place_order(request,total=0,quantity=0,): 
    current_user=request.user
    # # If the cart count is less than or equal to 0,then redirect back to store
    cart_Item=CartItem.objects.filter(user=current_user)
    cart_count=cart_Item.count()
    if cart_count<=0:
        return redirect('store')
    grand_total=0
    tax=0
    for cart_item in cart_Item:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax
    
  
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()
            orders=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            

            context={'order':orders,'cart_items':cart_Item,'tax':tax,'total':total,'grand_total':grand_total}      
            return render(request,'orders/payment.html',context)
    else:
        return redirect('checkout')


def view_payment(request):
    body=json.loads(request.body)
    print(body)
    order=Order.objects.get(user=request.user,order_number=body['orderID'],is_ordered=False)
    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'])
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()

    #Move the cart_item to OrderProduct Table
    cartItem=CartItem.objects.filter(user=request.user)
    for item in cartItem:
        orderProduct=OrderProduct()
        orderProduct.order_id=order.id
        orderProduct.payment=payment
        orderProduct.user_id=request.user.id
        orderProduct.product_id=item.product_id
        orderProduct.quantity=item.quantity
        orderProduct.product_price=item.product.price
        orderProduct.ordered=True
        orderProduct.save()



        # Adding the variations of items in order_product
        cart_items=CartItem.objects.get(id=item.id)
        product_variation=cart_items.variation.all()
        orderProduct=OrderProduct.objects.get(id=orderProduct.id)
        orderProduct.variation.set(product_variation)
        orderProduct.save()


        # reducing the quantity of sold Products
        product=products.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()


        # Now clearing the cart
    CartItem.objects.filter(user=request.user).delete()

    # Send Order received email to the customer
    mail_subject='ThankYou For Your Order'
    message=render_to_string('orders/order_received_email.html',{
        'user':request.user,
        'order':order,
    })
    to_email=request.user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    # Send Order number and transaction id back to sendData method via JSONResponse

    data={'order_number':order.order_number,'trans_id':payment.payment_id}
    return JsonResponse(data)

# Generating Order Complete page
def Order_Complete(request):
    order_number=request.GET.get('order_id')
    trans_id=request.GET.get('trans_id')
    try:
        orders=Order.objects.get(order_number=order_number,is_ordered=True)
        orderProduct=OrderProduct.objects.filter(order_id=orders.id)
        subtotal=0
        for items in orderProduct:
            subtotal+=items.product_price*items.quantity
        payment=Payment.objects.get(payment_id=trans_id)
        context={'orders':orders,'orderProduct':orderProduct,'order_number':orders.order_number,'trans_id':payment.payment_id,'status':payment.status,'subtotal':subtotal}
        return render(request,'orders/order_complete.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
    
    





    


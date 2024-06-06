from django.shortcuts import render,redirect
from .forms import *
from .models import *
from kart.models import *
import datetime
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def view_order(request,total=0,quantity=0,cart_items=None):
    grand_total=0
    tax=0

    current_user=request.user
    cart_items=Kart_item.objects.filter(user=request.user)
    if cart_items.count()<=0:
        return redirect('store')
    else:
        for item in cart_items:
            total+=item.product.price*item.quantity
            quantity+=item.quantity
        tax=(2*total)/100
        grand_total=total+tax
        

    if request.method=='POST':
        form=OrderForms(request.POST)
        if form.is_valid():
            data=order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.email=form.cleaned_data['email']
            data.phone=form.cleaned_data['phone']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.country=form.cleaned_data['country']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
    

            data.save()
            yr=int(datetime.date.today().strftime('%Y'))
            mt=int(datetime.date.today().strftime('%m'))
            dt=int(datetime.date.today().strftime('%d'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime('%Y%m%d')
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()
            orders=order.objects.get(order_number=order_number,user=current_user,is_ordered=False)

            context={'cart_items':cart_items,'order':orders,'tax':tax,'total':total,'grand_total':grand_total}
            return render(request,'orders/payment.html',context)
        else:
            return redirect('checkout')
        
def payment(request):
    current_user=request.user
    body=json.loads(request.body)
    print(body)
    Order=order.objects.get(order_number=body['orderid'],user=current_user,is_ordered=False)

    payment=Payment(
    user=current_user,
    payment_id=body['trans_id'],
    payment_method=body['payment_method'],
    status=body['status'],
    amount_paid=Order.order_total)
    payment.save()

    Order.payment=payment
    Order.is_ordered=True
    Order.save()


    #Move cart_iems to orderProducttable
    cart_items=Kart_item.objects.filter(user=current_user)
    for item in cart_items:
        orderdetails=orderdetail.objects.create(
            order_id=Order.id,
            user_id=current_user.id,
            payment=payment,
            product_id=item.product_id,
            product_price=item.product.price,
            quantity=item.quantity,
            ordered=True,)
        
        #adding Variations
        cart_items=Kart_item.objects.get(id=item.id)
        variations=cart_items.variations.all()
        orderdetailss=orderdetail.objects.get(id=orderdetails.id)
        orderdetailss.variations.set(variations)
        orderdetailss.save()

        # removing the stock of item from product table

        product=Products.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()

    cart_items=Kart_item.objects.filter(user=current_user)
    cart_items.delete()

    mail_subject="Order Confirmation"
    message=render_to_string('orders/order_confirmation.html',{
        'user':current_user,
        'order':Order, })
    to_email=current_user.email
    send_email=EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    data={'order_id':Order.order_number,'trans_id':payment.payment_id}
    return JsonResponse(data)
  

def order_complete(request):
    order_number=request.GET.get('order_id')
    trans_id=request.GET.get('trans_id')
    try:
        subtotal=0
        quantity=0
        Order=order.objects.get(order_number=order_number,user=request.user,is_ordered=True)
        order_product=orderdetail.objects.filter(order_id=Order.id)
        for item in order_product:
            subtotal+=item.product.price*item.quantity
            quantity+=item.quantity
        tax=(2*subtotal)/100
        grand_total=subtotal+tax
        payment=Payment.objects.get(payment_id=trans_id)
    except ObjectDoesNotExist:
        pass
    context={'order':Order,'Order_product':order_product,'Payment':payment,"sub_total":subtotal,'Grand_total':grand_total,"tax":tax}
    return render(request,'orders/order_complete.html',context)
    




from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login
from .models import account
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cartt.views import _cart_id
from cartt.models import cart,CartItem
from orders.models import *
import requests
# Create your views here.

def view_registeraton(request):
    if request.method=='POST':
        form=UserForms(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone=form.cleaned_data['phone']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            user=account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone=phone
            user.save()
            

            current_site=get_current_site(request)
            mail_subject='Account verification'
            message=render_to_string('accounts/account_verification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),})
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request, 'registeration successful')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=UserForms()
    context={'form':form,}
    return render(request,'accounts/register.html',context)


def view_Login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                Cart=cart.objects.get(cart_id=_cart_id(request))
                print("True Cart")
                is_cart_item_exist=CartItem.objects.filter(cart=Cart).exists()
                if is_cart_item_exist:
                    cart_item=CartItem.objects.filter(cart=Cart)
                    # Geting the product_variation by cart_id
                    product_variation=[]
                    for item in cart_item:
                        variations=item.variation.all()
                        product_variation.append(list(variations))
                    
                    # Get the cart items from the user to access his product variations
                    cart_item=CartItem.objects.filter(user=user)
                    ex_variation=[]
                    id=[]
                    for item in cart_item:
                        existing_variations=item.variation.all()
                        ex_variation.append(list(existing_variations))
                        id.append(item.id)
                        
                    for pr in product_variation:
                        if pr in ex_variation:
                            Index=ex_variation.index(pr)   
                            item_id=id[Index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user=user
                            item.save()
                        else:
                            cartItem=CartItem.objects.filter(cart=Cart)
                            for item in cartItem:
                                item.user=user
                                item.save()
                    
            except:
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            url=request.META.get('HTTP_REFERER')
            print(url)
            try:
                query=requests.utils.urlparse(url).query
                print(query)
                params=dict(x.split('=') for x in query.split('&'))
                print(params)
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)    
            except:
                 return redirect('dashboard')
            
        else:
            messages.error(request,'Invalid login Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url='login')
def view_Logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out successfully!')
    return redirect('login')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=account._default_manager.get(pk=uid)
    except (ValueError ,TypeError ,OverflowError, account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations,You account is activated')
        return redirect('login')
    else:
        messages.error(request,'Inavalid activation link')
        return redirect('register')


@login_required(login_url='login')   
def dashboard(request):
    order=Order.objects.order_by('created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count=order.count()

    user_profile=UserProfile.objects.get(user_id=request.user.id)
    context={'order_count':order_count,'user_profile':user_profile}


    return render(request,'accounts/dashboard.html',context)


def view_forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if account.objects.filter(email=email).exists():
            user=account.objects.get(email__iexact=email)
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('accounts/reset_password_email.html',{'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),})
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            

            messages.success(request,"Password reset email has been sent to your email address")
            return redirect('login')
        else:
            messages.success(request,"Account does not exist")
            return redirect('forgotpassword')
        
    return render(request,'accounts/forgotpassword.html')


def view_reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=account._default_manager.get(pk=uid)
    except (TypeError ,ValueError, OverflowError, account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return  redirect('resetpassword')
    else:
        messages.error(request,'The link has been expired')
        # return redirect('login')
    return redirect('login')

def view_resetpassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            uid=request.session.get('uid')
            user=account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password has been reset successfully!')
            return redirect('login')
        else:
            messages.error('password and confirm password do not match!')
            return redirect('resetpassword')
    return render(request,'accounts/resetpassword.html')


@login_required(login_url='login')
def view_myOrders(request):
    order=Order.objects.filter(user_id=request.user.id,is_ordered=True).order_by('-created_at')
    context={'orders':order}
    return render(request,'accounts/myorders.html',context)

@login_required(login_url='login')
def view_editprofile(request):
    userProfile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        userform=UserForms(request.POST,instance=request.user)
        userProfileform=UserProfileForms(request.POST,request.FILES,instance=userProfile)
        if userform.is_valid() and userProfileform.is_valid():
            userform.save()
            userProfileform.save()
            messages.success(request,'Your Profile has been successfully updated')
            return redirect('edit_profile')
    else:
        userform=UserForms(instance=request.user)
        userProfileform=UserProfileForms(instance=userProfile)
    context={'userform':userform,'userProfileform':userProfileform,'userprofile':userProfile}
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='login')
def view_changePassword(request):
    if request.method=='POST':
        current_password=request.POST["current_password"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm password"]

        user=account.objects.get(username__exact=request.user.username)
        if  password == confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(password)
                user.save()
                messages.success(request,'Your Password has been successfully updated!')
                return redirect('changePassword')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('changePassword')
        else:
            messages.error(request,'Password and confirm Password does not match')
            return redirect('changePassword')
    return render(request,'accounts/changePassword.html')
 

def view_orderdetail(request,order_id):
    order_product=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    sub_total=0
    for item in order_product:
        sub_total+=item.product.price*item.quantity
    
    
    context={'order_product':order_product,'orders':order,'order_number':order_id,'sub_total':sub_total}
    return render(request,'accounts/orderdetail.html',context)


































































































































































































































































































































































































































































 
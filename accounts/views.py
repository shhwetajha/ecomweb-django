from django.shortcuts import render
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from kart.models import *
from kart.views import _kart_id
import requests
from django.shortcuts import get_object_or_404
from accounts.models import *
from orders.models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def view_register(request):
    if request.method=='POST':
        forms=UserForms(request.POST)
        if forms.is_valid():
            first_name=forms.cleaned_data['first_name']
            last_name=forms.cleaned_data['last_name']
            email=forms.cleaned_data['email']
            username=email.split('@')[0]
            password=forms.cleaned_data['password']
            phone=forms.cleaned_data['phone']
            user=account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone=phone
            user.save()
            current_site=get_current_site(request)
            mail_subject='Account Verification'
            message=render_to_string('accounts/account_verification.html',{'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token((user))})
            to_email=email
            send_email=EmailMessage(mail_subject, message,to=[to_email])
            send_email.send()
            # messages.success(request,'registeration has been successfully done!')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        forms=UserForms()
    context={'forms':forms}
    return render(request,'accounts/register.html',context)

def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=account._default_manager.get(pk=uid)
    except (ValueError,TypeError,OverflowError,account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('login')
    else:
        return render(request,'accounts/register.html')


def view_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Kart.objects.get(kart_id=_kart_id(request))
                cartitemexist=Kart_item.objects.filter(cart=cart).exists()
                if cartitemexist:
                    cart_item=Kart_item.objects.filter(cart=cart)
                    ex_variation=[]
                    ex_id=[]
                    for item in cart_item:
                        Variations=item.variations.all()
                        ex_variation.append(list(Variations))
                        ex_id.append(item.id)
                   
                
                    cart_item_login=Kart_item.objects.filter(user=user)
                    ex_var=[]
                    exx_id=[]
                    for item in cart_item_login:
                        Variationss=item.variations.all()
                        ex_var.append(list(Variationss))
                        exx_id.append(item.id)

                    for pr in ex_variation:
                        if pr in ex_var:
                            Index=ex_var.index(pr)
                            var_id=exx_id[Index]
                            cart_itemm=Kart_item.objects.get(user=user,id=var_id)
                            cart_itemm.quantity+=1
                            cart_itemm.user=user
                            cart_itemm.save()
                        else:
                            kartt=Kart_item.objects.filter(cart=cart)
                            for item in kartt:
                                item.user=user
                                item.save()
            except:
                pass
            auth.login(request,user)
            try:
                url=request.META.get('HTTP_REFERER')
                query=requests.utils.urlparse(url).query
                params=dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)
            except:
                return redirect('dashboard')
        else:
            return redirect('login')

    return render(request,'accounts/login.html')       

@login_required(login_url='login')
def view_logout(request):
    auth.logout(request)
    messages.error(request,'user logged out successfully!')
    return redirect('login')

def view_forgotpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if account.objects.filter(email=email).exists():
            user=account.objects.get(email__iexact=email)
            current_site=get_current_site(request)
            mail_subject='Forgot Password Verification'
            message=render_to_string('accounts/forgot_password_verification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),})
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            messages.success(request,'A reset password verification email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'email does not exist')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')

def reset_password_validate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=account._default_manager.get(pk=uid)
    except(ValueError,OverflowError,TypeError,account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Reset Your Password')
        return redirect('resetpassword')
    else:
        messages.error(request,'Invalid Activation link')
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
            messages.success(request,'password changed successfully!')
            return redirect('login')
        else:
            messages.error(request,'password and confirm password do not match')
            return redirect('resetpassword')
    return render(request,'accounts/resetpassword.html')


@login_required(login_url='login')
def view_dashboard(request):
    orders=order.objects.order_by('created_at').filter(user=request.user,is_ordered=True)
    order_count=orders.count()
    try:
        userprofile=UserProfile.objects.get(user=request.user)
    except:
        userprofile=None
    context={'orders':orders,'order_count':order_count,'userprofile':userprofile}
    return render(request,'accounts/dashboard.html',context)

def view_myorders(request):
    Order=order.objects.order_by('created_at').filter(user=request.user,is_ordered=True)
    context={'Order':Order}
    return render(request,'accounts/myorders.html',context)

def view_orderdetail(request,order_number):
    Order=order.objects.get(order_number=order_number)
    Order_product=orderdetail.objects.filter(order_id=Order.id)
    sub_total=0
    for orders in Order_product:
        sub_total+=orders.product.price*orders.quantity
    context={'order_product':Order_product,'sub_total':sub_total,'order':Order}
    return render(request,'accounts/orderdetails.html',context)


@login_required(login_url='login')
def view_editprofile(request):
        userprofile=get_object_or_404(UserProfile,user=request.user)
        if request.method=='POST':
            userform=userForms(request.POST,instance=request.user)
            userprofileform=UserProfileForm(request.POST,request.FILES,instance=userprofile)
            if userform.is_valid() and userprofileform.is_valid():
                userform.save()
                userprofileform.save()
                messages.success(request,'Your profile has been successfully updated')
                return redirect('editprofile')
        else:
            userform=userForms(instance=request.user)
            userprofileformm=UserProfileForm(instance=userprofile)  
        context={'userforms':userform,'userprofileforms':userprofileformm,'userprofile':userprofile}
        return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='login')
def view_changepassword(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        user=account.objects.get(username__exact=request.user.username)
        if password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(password)
                user.save()
                messages.success(request,'password has been successfully updated!')
                return redirect('change_password')
            else:
                messages.error(request,'current password do not match!')
                return redirect('change_password')
        else:
            messages.error(request,'password and confirm password do not match!')
            return redirect('change_password')


    return render(request,'accounts/changepassword.html')


def view_pdfupdate(request):
    return render(request,'accounts/pdfexport.html')


from django.shortcuts import render, redirect
from .models import Country, State, City
from .forms import LocationForm, SuggestionForm
from django.http import JsonResponse

def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country']
            state_name = form.cleaned_data['state']
            city_name = form.cleaned_data['city']
            
            state, created = State.objects.get_or_create(name=state_name, country=country)
            City.objects.get_or_create(name=city_name, state=state)
            
            return redirect('statecity')
    else:
        form = LocationForm()
    return render(request, 'statecity.html', {'form': form})

def suggest_location(request):
    form = SuggestionForm()
    return render(request, 'accounts/location.html', {'form': form})

def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(states.values('id', 'name')), safe=False)

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


def create_location(request):
    if request.method =='POST':
        country=request.POST.get('country')
        state=request.POST.get('state')
        city=request.POST.get('city')


        count=Country.objects.create(name=country)
        stat=State.objects.create(name=state,country=count)
        cit=City.objects.create(name=city,state=stat)
        return render(request,'statecity.html')
    else:
        return render(request,'statecity.html')
    
def view_location(request):
    country=Country.objects.all()
    context={'countries':country}
    return render(request,'viewcountrydet.html',context)


def get_states(request):
    country_id=request.GET['country_id']
    # get_country=Country.objects.get(id=country_id)
    state=State.objects.filter(country_id=country_id)
    context={"state":state}
    print('********************')
    return render(request,'get-states.html',context)



def get_cities(request):
    state_id=request.GET['state_id']
    cities=City.objects.filter(state_id=state_id)
    context={'cities':cities}
    return render(request,'get-cities.html',context)


def dependent_field(request):
    country_id=request.GET.get('country',None)
    state_id=request.GET.get('state',None)
    state=None
    city=None
    if country_id:
        state=State.objects.filter(country_id=country_id)
    if state_id:
        city=City.objects.filter(state_id=state_id)
    country=Country.objects.all()
    context={'countries':country,'state':state,'city':city}
    return render(request,'dependentfield.html',context)



# views.py
# views.py
from django.shortcuts import render
from django.http import HttpResponse

def dynamic_form(request):
    if request.method == 'POST':
        from_initial = request.POST.get('from_initial', None)
        to_initial = request.POST.get('to_initial', None)
        from_final = request.POST.get('from_final', None)
        to_final = request.POST.get('to_final', None)

        return HttpResponse(f'Initial From: {from_initial}, Initial To: {to_initial}<br>Final From: {from_final}, Final To: {to_final}')
    
    # If initial GET request or form not submitted yet
    initial_from_value = 0
    initial_to_value = 10
    context = {
        'initial_from_value': initial_from_value,
        'initial_to_value': initial_to_value
    }
    return render(request, 'accounts/dynamic_form.html', context)

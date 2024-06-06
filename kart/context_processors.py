from .models import *
from .views import _kart_id
from django.core.exceptions import ObjectDoesNotExist

 
def counter(request):
    count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart=Kart.objects.filter(kart_id=_kart_id(request))
            if request.user.is_authenticated:
                cart_items=Kart_item.objects.all().filter(user=request.user)
            else:
                cart_items=Kart_item.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                count+=item.quantity
            return dict(count=count)
        except ObjectDoesNotExist:
            count=0

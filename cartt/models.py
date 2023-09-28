from django.db import models
from store.models import *
from accounts.models import *

# Create your models here.
class cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user=models.ForeignKey(account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    cart=models.ForeignKey(cart,on_delete=models.CASCADE,null=True)
    variation=models.ManyToManyField(Variation,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price*self.quantity


    def __unicode__(self):
        return self.product

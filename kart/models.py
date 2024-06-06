from django.db import models
from store.models import *
from accounts.models import *

# Create your models here.
class Kart(models.Model):
    kart_id=models.CharField(max_length=100,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.kart_id
    

class Kart_item(models.Model):
    cart=models.ForeignKey(Kart,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(account,on_delete=models.CASCADE,null=True)
    variations=models.ManyToManyField(variations,blank=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)


    def sub_total(self):
        return self.product.price*self.quantity


    def __unicode__(self):
        return self.product


class Student(models.Model):
    name=models.CharField(max_length=100)
    rank=models.IntegerField()
    





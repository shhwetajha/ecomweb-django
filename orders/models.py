from django.db import models
from accounts.models import *
from store.models import *
# Create your models here.


class Payment(models.Model):
    user=models.ForeignKey(account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

STATUS=(('new','new'),
        ('accepted','accepted'),
        ('completed','completed'),
        ('cancelled','cancelled'),)
class order(models.Model):
    user=models.ForeignKey(account,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address_line_1=models.CharField(max_length=100)
    address_line_2=models.CharField(max_length=100,blank=True,default='-')
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    order_note=models.CharField(max_length=100)
    order_total=models.FloatField()
    status=models.CharField(choices=STATUS,max_length=100,default='new')
    ip=models.CharField(max_length=100)
    tax=models.FloatField()
    order_number=models.CharField(max_length=100)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

      
    
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'


    def __str__(self):
        return self.user.first_name


class orderdetail(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.ForeignKey(account,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variations=models.ManyToManyField(variations,blank=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.product_name


from django.db import models 
from great.models import categories
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from accounts.models import *
from django.db.models import Avg,Count

# Create your models here.
class Products(models.Model):
    product_name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=100,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='store/products')
    stock=models.IntegerField()
    categories=models.ForeignKey(categories,on_delete=models.CASCADE)
    is_available=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name='Product'
        verbose_name_plural='Products'


    def get_url(self):
        return reverse('product_det',args=[self.categories.slug,self.slug])


    def average_review(self):
        reviewrating=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviewrating['average'] is not None:
            avg=float(reviewrating['average'])
        return avg
        
    def average_count(self):
        avgcount=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if avgcount['count'] is not None:
            count=int(avgcount['count'])
        return count

    def __str__(self):
        return self.product_name


class variationmanager(models.Manager):
    def colors(self):
        return super(variationmanager,self).filter(variation_category='colors')
    def sizes(self):
        return super(variationmanager,self).filter(variation_category='sizes')

    
    
        
variation_category_choice=(
    ('colors','colors'),
    ('sizes','sizes'),
     
)
class variations(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_Active=models.BooleanField(default=True)   
    created_date=models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name='variation'
        verbose_name_plural='variations'
    objects=variationmanager()


    def __str__(self):
        return self.variation_value


class ProductGallery(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,default=None)
    images=models.ImageField(upload_to='photos/products',max_length=100)


    class Meta:
        verbose_name='ProductGallery'
        verbose_name_plural='ProductGalleries'


    def __str__(self):
        return self.product.product_name

class ReviewRating(models.Model):
    user=models.ForeignKey(account,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    subject=models.CharField(blank=True,max_length=100)
    review=models.TextField(blank=True,max_length=100)
    rating=models.FloatField()
    ip=models.CharField(blank=True,max_length=100)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject


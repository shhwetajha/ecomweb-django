from django.db import models
from ecomapp.models import *
from django.urls import reverse
from accounts.models import *
from django.db.models import Avg,Count
# Create your models here.

class products(models.Model):
    product_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=50,unique=True)
    description=models.CharField(max_length=200,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='product'
        verbose_name_plural='products'

    def averageReview(self):
        review=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if review['average'] is not None:
            avg=float(review['average'])
            return avg
        


    def AverageReviewCount(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
            return count
    def get_url(self):
        return reverse('product_detail' ,args=[self.category.slug,self.slug])
    



    def __str__(self):
        return self.product_name
    


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active='True')
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active='True')


variation_category_choice=(
    ('color','color'),
    ('size','size'),
)


class Variation(models.Model):
    Products=models.ForeignKey(products,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VariationManager()

    def __str__(self):
        return self.variation_value

class ReviewRating(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    user=models.ForeignKey(account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=200,blank=True)
    review=models.TextField(max_length=200,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.subject
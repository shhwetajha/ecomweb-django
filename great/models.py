from django.db import models
from django.urls import reverse

# Create your models here.
class categories(models.Model):
    category_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=100,null=True)
    images=models.ImageField(upload_to='photos/categories')


    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'


    def get_url(self):
        return reverse('categories_det',args=[self.slug])

    def __str__(self):
        return self.category_name


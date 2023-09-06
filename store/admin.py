from django.contrib import admin
from store.models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','category','stock','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}



admin.site.register(products,ProductAdmin)

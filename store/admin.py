from django.contrib import admin
from store.models import *
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=ProductGallery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','category','stock','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}
    inlines=[ProductGalleryInline]





class VariationAdmin(admin.ModelAdmin):
    list_display=['Products','variation_category','variation_value','is_active']
    list_editable=('is_active',)
    list_filter=['Products','variation_category','variation_value','is_active']



admin.site.register(products,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)


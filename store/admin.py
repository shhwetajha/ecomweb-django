from django.contrib import admin
from .models import *
import admin_thumbnails


# Register your models here.
@admin_thumbnails.thumbnail('images')
class ProductGalleryInline(admin.TabularInline):
    model=ProductGallery
    extra=1


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=['product_name','slug','price','description','images','categories','stock','is_available']
    inlines=[ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_Active']
    list_filter=['product','variation_category','variation_value','is_Active']
    list_editable=['is_Active']

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display=['user','product','subject','review','rating','status','ip']


admin.site.register(Products,ProductAdmin)
admin.site.register(variations,VariationAdmin)
admin.site.register(ProductGallery)
admin.site.register(ReviewRating,ReviewRatingAdmin)

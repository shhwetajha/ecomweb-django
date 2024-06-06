from django.contrib import admin
from .models import *

# Register your models here.
class KartAdmin(admin.ModelAdmin):
    list_display=['kart_id','date_added']


class KartItemAdmin(admin.ModelAdmin):
    list_display=['user','product','quantity','is_active']

admin.site.register(Kart,KartAdmin)
admin.site.register(Kart_item,KartItemAdmin)
admin.site.register(Student)
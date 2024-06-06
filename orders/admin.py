from django.contrib import admin
from .models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','address_line_1','address_line_2','state','city','country','phone','email','is_ordered','ip','order_number','order_note']

class PaymentAdmin(admin.ModelAdmin):
    list_display=['payment_id','payment_method','amount_paid','status']

class OrderdetailAdmin(admin.ModelAdmin):
    list_display=['product_price','quantity','ordered']

admin.site.register(order,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(orderdetail,OrderdetailAdmin)
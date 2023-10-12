from django.contrib import admin
from orders.models import Payment,Order,OrderProduct

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    readonly_fields=('payment','user','product','quantity','product_price','ordered')
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['full_name','order_number','email','address_line_1','phone','status','is_ordered',
    'city','tax','order_total','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','email','phone']
    list_per_page=20
    inlines=[OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)

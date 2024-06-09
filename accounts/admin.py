
# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=['first_name','last_name','username','date_joined','last_login']
    list_display_links=['first_name','last_name','username']
    readonly_fields=['date_joined','last_login']
    ordering=['-date_joined']
    filter_horizontal=()
    list_filter=()
    fieldsets=()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html("<img src='{}' width='30' style='border-radius:50%'".format(object.profile_picture.url))
    thumbnail.short_description="profile picture"
    list_display=['thumbnail','user','address_line_1','address_line_2','state','city','country','profile_picture']




    #  return format_html('<img src="{}" width="30" style="border-radius:50%"'.format(object.profile_picture.url))
admin.site.register(account,AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Country)


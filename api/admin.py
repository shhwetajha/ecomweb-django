from django.contrib import admin
from api.models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
        list_display=['name','age','phone']

admin.site.register(Student,StudentAdmin)


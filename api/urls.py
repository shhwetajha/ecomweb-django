from django.urls import path,include
from api.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('stuapi',Student_view,basename='studentapi')


urlpatterns=[
    path('',include(router.urls))

]
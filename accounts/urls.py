from django.urls import path
from .views import *
urlpatterns=[
    path('',view_register,name='register'),
    path('activate/<uid64>/<token>/',activate,name='activate'),
    path('login/',view_login,name='login'),
    path('logout/',view_logout,name='logout'),
    path('forgotpassword/',view_forgotpassword,name='forgotpassword'),
    path('forgotpassword_validate/<uid64>/<token>/',reset_password_validate,name='reset_password_validate'),
    path('reset_password/',view_resetpassword,name='resetpassword'),
    path('dashboard/',view_dashboard,name='dashboard'),
    path('edit_profile/',view_editprofile,name='editprofile'),
    path('myOrders/',view_myorders,name='myOrders'),
    path('orderdetail/<int:order_number>/',view_orderdetail,name='orderdetail'),
    path('change_password/',view_changepassword,name='change_password'),
    path('pdfupdate/',view_pdfupdate,name='pdfupdate')
    

]
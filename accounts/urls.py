from django.urls import path
from .views import *

urlpatterns=[
    path("registeration/",view_registeraton,name="register"),
    path("login/",view_Login,name="login"),
    path("Logout/",view_Logout,name="logout"),
    path("activate/<uidb64>/<token>/",activate,name="activate"),
    path('dashboard/',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    path("forgot_password/",view_forgotpassword,name="forgotpassword"),
    path("reset_password/<uidb64>/<token>/",view_reset_password_validate,name='resetpasswordvalidate'),
    path('resetpassword/', view_resetpassword,name='resetpassword'),
    path('myorders/',view_myOrders,name='myOrders'),
    path('edit_profile/',view_editprofile,name='edit_profile'),
    path('change_password/',view_changePassword,name='changepassword'),
    path('order_detail/<int:order_id>/',view_orderdetail,name='order_detail')
]
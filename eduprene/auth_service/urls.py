from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('resend_register_otp/', views.resend_register_otp, name='resend_register_otp')
]
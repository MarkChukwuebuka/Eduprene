from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('resend_register_otp/', views.resend_register_otp, name='resend_register_otp'),
    path('verify_registration_otp/', views.verify_registration_otp, name='verify_registration_otp')
]
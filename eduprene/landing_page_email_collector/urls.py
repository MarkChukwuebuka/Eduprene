from django.urls import path
from . import views

urlpatterns = [
    path('email_collector/', views.email, name='email_collector')
]
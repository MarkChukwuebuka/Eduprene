from django.contrib import admin
from .models import Banks, UserBankAccount

admin.site.register(Banks)
admin.site.register(UserBankAccount)
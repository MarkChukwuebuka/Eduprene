from django.contrib import admin

# Register your models here.
from .models import  RegisterLogs, User, UserAccount, UserSubscriptions, Referral

admin.site.register(RegisterLogs)
admin.site.register(User)
admin.site.register(UserAccount)
admin.site.register(UserSubscriptions)
admin.site.register(Referral)
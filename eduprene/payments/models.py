import uuid

from django.db import models
from django.utils import timezone

from auth_service.models import User


# Create your models here.
class Banks(models.Model):
    bank_name = models.CharField(max_length=250, null=False)
    bank_code = models.CharField(max_length=10, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Banks"


class UserBankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=11, null=True)
    account_name = models.CharField(max_length=100, null=True)
    bank = models.ForeignKey(Banks, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "User's Bank Accounts"

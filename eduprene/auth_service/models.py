import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from constants.other_constants import SUBSCRIPTION_STATUS, REFERRAL_STATUS
from subscriptions.models import Subscription


class RegisterLogs(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    otp = models.CharField(max_length=100, null=False)
    otp_requested_at = models.DateTimeField(null=False)
    otp_verified = models.BooleanField(default=False)
    otp_trials = models.IntegerField(default=0)

    referred_by = models.CharField(max_length=10, default=None, null=True)

    class Meta:
        verbose_name_plural = "Register Logs"


class User(AbstractUser):
    uid = models.CharField(max_length=36, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4().hex)
        super().save(*args, **kwargs)


class UserAccount(models.Model):
    SUBSCRIPTION_STATUS_CHOICES = [(i, SUBSCRIPTION_STATUS[i]) for i in SUBSCRIPTION_STATUS]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0, null=True)
    subscription_status = models.CharField(max_length=15, default=SUBSCRIPTION_STATUS['NOT_ACTIVE'], choices=SUBSCRIPTION_STATUS_CHOICES)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "User's Accounts"


class UserSubscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Users Subscriptions"


class Referral(models.Model):
    REFERRAL_STATUS_CHOICES = [(i, REFERRAL_STATUS[i]) for i in REFERRAL_STATUS]

    referrer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    related_name="refers")  # User that referred
    referred_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
                                       related_name="referred")  # User that was referred
    status = models.CharField(max_length=10, default=REFERRAL_STATUS['PENDING'],
                              choices=REFERRAL_STATUS_CHOICES)  # Determines if a referrer has been paid

    created_at = models.DateTimeField(default=timezone.now)

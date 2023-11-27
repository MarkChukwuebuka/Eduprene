from django.db import models
from django.utils import timezone


# Create your models here.
class Emails(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    first_name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=50, null=False, unique=True)
    referral_code = models.CharField(max_length=12, null=False, unique=True)
    referred_by = models.CharField(max_length=12, null=True, default=None)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Emails"
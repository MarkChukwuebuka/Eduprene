from django.db import models
from django.utils import timezone


# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=250, null=False)
    amount = models.FloatField(default=0.0, null=True)

    created_at = models.DateTimeField(default=timezone.now)

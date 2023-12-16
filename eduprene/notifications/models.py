from django.db import models
from django.utils import timezone


# Create your models here.
class Notification(models.Model):
    email = models.CharField(max_length=50, null=True)
    channel = models.CharField(max_length=15, null=True)
    event = models.CharField(max_length=50, null=False)
    data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
from django.db import models

# Create your models here.
class LandingPageUser(models.Model):

    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    referred_by = models.CharField(max_length=50, null=True, blank=True)
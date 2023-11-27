from rest_framework import serializers
from .models import Emails

class EmailCollectorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    referral_code = serializers.CharField(read_only=True)

    class Meta:
        model = Emails
        fields = ["id", "email", "first_name", "referred_by", "referral_code"]

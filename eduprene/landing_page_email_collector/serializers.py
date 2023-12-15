from django.db.models import Q
from rest_framework import serializers
from .models import Emails


class EmailCollectorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    referral_code = serializers.CharField(read_only=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = Emails
        fields = ["id", "email", "first_name", "referred_by", "referral_code"]


    def validate(self, data):
        """
        Validate that the email is unique.
        """
        email = data.get('email').lower().strip()

        # The queryset checks for uniqueness
        queryset = Emails.objects.filter(Q(email__iexact=email))

        # Exclude the current instance when updating
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        return data
from password_validator import PasswordValidator
from rest_framework import serializers

from auth_service.models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_password(self, value):
        """ Checks and verifies that password is secure
            Password must have minimum of 6 characters, have an uppercase, a lowercase, a number, and a symbol
        """
        schema = PasswordValidator()
        schema.min(6).uppercase().lowercase().digits().symbols()

        if not schema.validate(value):
            raise serializers.ValidationError(
                'Password not secure! Must contain minimum of 6 characters, an uppercase, a lowercase, a number, '
                'and a symbol')

        password = make_password(value)
        return password


class RegisterSerializerResponse(serializers.Serializer):
    email = serializers.CharField()

class ResendRegisterOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
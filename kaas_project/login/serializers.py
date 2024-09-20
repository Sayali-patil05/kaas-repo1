from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "mobile_number",
            "role_id",
            "aaas_uid",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile_number = serializers.CharField()
    reference_number = serializers.IntegerField(
        min_value=100000, max_value=999999, required=False, allow_null=True
    )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField()

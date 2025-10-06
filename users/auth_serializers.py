from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from users.models import User, District, VerificationCode, PasswordResetToken


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name',
                  'phone_number', 'user_type']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            user_type=validated_data['user_type'],
            is_active=False  # User needs to verify before activation
        )
        return user


class PhoneVerificationSerializer(serializers.Serializer):
    """
    Serializer for phone verification.
    """
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Code must be a 6-digit number.")
        return value


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Code must be a 6-digit number.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    token = serializers.CharField(max_length=64)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class AccountStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for account verification status.
    """
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'phone_verified', 'email_verified',
                  'is_active', 'is_account_locked']
        read_only_fields = fields


class AccountRecoverySerializer(serializers.Serializer):
    """
    Serializer for account recovery.
    """
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=15)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'], phone_number=attrs['phone_number'])
            if not user.is_account_locked:
                raise serializers.ValidationError("Account is not locked.")
        except User.DoesNotExist:
            raise serializers.ValidationError("No matching account found.")
        return attrs


class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer for Rwanda districts.
    """
    class Meta:
        model = District
        fields = ['id', 'name', 'code', 'province']
        read_only_fields = fields


class ResendVerificationSerializer(serializers.Serializer):
    """
    Serializer for resending verification codes.
    """
    email = serializers.EmailField()
    verification_type = serializers.ChoiceField(choices=['phone', 'email'])

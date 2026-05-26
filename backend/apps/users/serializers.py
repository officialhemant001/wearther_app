"""
User serializers for authentication, profiles, and device management.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta
from .models import User, UserProfile, UserDevice, OTPVerification
from apps.core.utils import generate_otp


# ==================================================
# Auth Serializers
# ==================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with extra user data in claims."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['is_premium'] = user.profile.is_premium if hasattr(user, 'profile') else False
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserMinimalSerializer(self.user).data
        return data


class SignupSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'phone_number']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Email + password login."""
    email = serializers.EmailField()
    password = serializers.CharField()


class OTPRequestSerializer(serializers.Serializer):
    """Request an OTP code."""
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    purpose = serializers.ChoiceField(
        choices=['login', 'signup', 'verify_email', 'verify_phone', 'reset_password']
    )

    def validate(self, attrs):
        if not attrs.get('phone_number') and not attrs.get('email'):
            raise serializers.ValidationError('Either phone_number or email is required.')
        return attrs


class OTPVerifySerializer(serializers.Serializer):
    """Verify an OTP code."""
    otp_code = serializers.CharField(max_length=6)
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    purpose = serializers.ChoiceField(
        choices=['login', 'signup', 'verify_email', 'verify_phone', 'reset_password']
    )


class GoogleAuthSerializer(serializers.Serializer):
    """Google OAuth token."""
    token = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    """Request password reset."""
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Confirm password reset with OTP."""
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8, validators=[validate_password])


class ChangePasswordSerializer(serializers.Serializer):
    """Change password (authenticated)."""
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value


class EmailVerifySerializer(serializers.Serializer):
    """Verify email with OTP."""
    otp_code = serializers.CharField(max_length=6)


# ==================================================
# User/Profile Serializers
# ==================================================

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user data for token responses."""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_email_verified']


class UserProfileSerializer(serializers.ModelSerializer):
    """Full user profile serializer."""
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'location', 'latitude', 'longitude',
            'temperature_unit', 'wind_speed_unit', 'theme',
            'push_notifications', 'email_notifications', 'sms_notifications',
            'alert_notifications', 'daily_forecast_email',
            'aqi_alerts_enabled', 'aqi_threshold',
            'is_premium', 'premium_expires_at',
        ]
        read_only_fields = ['is_premium', 'premium_expires_at']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with profile."""
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'phone_number',
            'is_email_verified', 'is_phone_verified',
            'auth_provider', 'created_at', 'profile',
        ]
        read_only_fields = ['id', 'email', 'auth_provider', 'created_at']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data and hasattr(instance, 'profile'):
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()

        return instance


class UserDeviceSerializer(serializers.ModelSerializer):
    """User device/session serializer."""
    class Meta:
        model = UserDevice
        fields = ['id', 'device_name', 'device_type', 'ip_address', 'last_active', 'is_active', 'created_at']
        read_only_fields = ['id', 'ip_address', 'last_active', 'created_at']


class UserSettingsSerializer(serializers.ModelSerializer):
    """User settings (profile preferences subset)."""
    class Meta:
        model = UserProfile
        fields = [
            'temperature_unit', 'wind_speed_unit', 'theme',
            'push_notifications', 'email_notifications', 'sms_notifications',
            'alert_notifications', 'daily_forecast_email',
            'aqi_alerts_enabled', 'aqi_threshold',
        ]

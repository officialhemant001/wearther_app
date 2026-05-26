"""
Authentication and user management views.
"""

from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from .models import User, UserProfile, UserDevice, OTPVerification
from .serializers import (
    SignupSerializer, LoginSerializer, CustomTokenObtainPairSerializer,
    OTPRequestSerializer, OTPVerifySerializer, GoogleAuthSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    ChangePasswordSerializer, EmailVerifySerializer,
    UserDetailSerializer, UserProfileSerializer, UserSettingsSerializer,
    UserDeviceSerializer, UserMinimalSerializer,
)
from apps.core.utils import generate_otp, get_client_ip, get_user_agent, success_response


# ==================================================
# Authentication Views
# ==================================================

class SignupView(generics.CreateAPIView):
    """Register a new user account."""
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Send verification email OTP
        otp = generate_otp()
        OTPVerification.objects.create(
            user=user,
            email=user.email,
            otp_code=otp,
            purpose='verify_email',
            expires_at=timezone.now() + timedelta(minutes=15),
        )

        return Response(
            success_response(
                data={
                    'user': UserMinimalSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                },
                message='Account created successfully. Please verify your email.',
            ),
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Authenticate user with email and password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

        if not user:
            return Response(
                {'success': False, 'error': {'message': 'Invalid email or password.'}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'success': False, 'error': {'message': 'Account is deactivated.'}},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Update last login info
        user.last_login_ip = get_client_ip(request)
        user.save(update_fields=['last_login_ip', 'last_login'])

        # Register device
        UserDevice.objects.update_or_create(
            user=user,
            user_agent=get_user_agent(request),
            defaults={
                'device_name': request.data.get('device_name', 'Unknown Device'),
                'device_type': request.data.get('device_type', 'other'),
                'ip_address': get_client_ip(request),
                'is_active': True,
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response(success_response(
            data={
                'user': UserDetailSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            },
            message='Login successful.',
        ))


class LogoutView(APIView):
    """Blacklist the refresh token to logout."""
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(success_response(message='Logged out successfully.'))
        except Exception:
            return Response(success_response(message='Logged out.'))


class OTPRequestView(APIView):
    """Request an OTP code for various purposes."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_code = generate_otp()
        data = serializer.validated_data

        # Find user if exists
        user = None
        if data.get('email'):
            user = User.objects.filter(email=data['email']).first()
        elif data.get('phone_number'):
            user = User.objects.filter(phone_number=data['phone_number']).first()

        OTPVerification.objects.create(
            user=user,
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            otp_code=otp_code,
            purpose=data['purpose'],
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        # In production, send via Twilio/email. For dev, log to console.
        print(f"[OTP] Code: {otp_code} for {data.get('email') or data.get('phone_number')}")

        return Response(success_response(
            message='OTP sent successfully.',
            data={'expires_in': 600},
        ))


class OTPVerifyView(APIView):
    """Verify an OTP code."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Find the OTP record
        filters = {'otp_code': data['otp_code'], 'purpose': data['purpose'], 'is_used': False}
        if data.get('email'):
            filters['email'] = data['email']
        elif data.get('phone_number'):
            filters['phone_number'] = data['phone_number']

        otp = OTPVerification.objects.filter(**filters).order_by('-created_at').first()

        if not otp or not otp.is_valid():
            return Response(
                {'success': False, 'error': {'message': 'Invalid or expired OTP.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.is_used = True
        otp.save()

        # Handle different purposes
        if data['purpose'] == 'login':
            user = otp.user
            if not user and data.get('phone_number'):
                user = User.objects.filter(phone_number=data['phone_number']).first()
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(success_response(
                    data={
                        'user': UserDetailSerializer(user).data,
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                        },
                    },
                    message='OTP verified. Login successful.',
                ))
            return Response(
                {'success': False, 'error': {'message': 'User not found.'}},
                status=status.HTTP_404_NOT_FOUND,
            )

        elif data['purpose'] == 'verify_email':
            if otp.user:
                otp.user.is_email_verified = True
                otp.user.save(update_fields=['is_email_verified'])
            return Response(success_response(message='Email verified successfully.'))

        elif data['purpose'] == 'verify_phone':
            if otp.user:
                otp.user.is_phone_verified = True
                otp.user.save(update_fields=['is_phone_verified'])
            return Response(success_response(message='Phone verified successfully.'))

        return Response(success_response(
            message='OTP verified.',
            data={'verified': True},
        ))


class GoogleAuthView(APIView):
    """Authenticate with Google OAuth token."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            from google.oauth2 import id_token
            from google.auth.transport import requests as google_requests
            from django.conf import settings

            idinfo = id_token.verify_oauth2_token(
                serializer.validated_data['token'],
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

            email = idinfo.get('email')
            name = idinfo.get('name', '')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': name.split(' ')[0] if name else '',
                    'last_name': ' '.join(name.split(' ')[1:]) if name else '',
                    'is_email_verified': True,
                    'auth_provider': 'google',
                },
            )

            refresh = RefreshToken.for_user(user)
            return Response(success_response(
                data={
                    'user': UserDetailSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    'is_new_user': created,
                },
                message='Google authentication successful.',
            ))

        except Exception as e:
            return Response(
                {'success': False, 'error': {'message': f'Google authentication failed: {str(e)}'}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetRequestView(APIView):
    """Request a password reset OTP."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if user:
            otp_code = generate_otp()
            OTPVerification.objects.create(
                user=user,
                email=user.email,
                otp_code=otp_code,
                purpose='reset_password',
                expires_at=timezone.now() + timedelta(minutes=15),
            )
            print(f"[PASSWORD RESET] OTP: {otp_code} for {user.email}")

        # Always return success to prevent email enumeration
        return Response(success_response(
            message='If the email exists, a reset code has been sent.',
        ))


class PasswordResetConfirmView(APIView):
    """Reset password using OTP."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        otp = OTPVerification.objects.filter(
            email=data['email'],
            otp_code=data['otp_code'],
            purpose='reset_password',
            is_used=False,
        ).order_by('-created_at').first()

        if not otp or not otp.is_valid():
            return Response(
                {'success': False, 'error': {'message': 'Invalid or expired reset code.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.is_used = True
        otp.save()

        user = User.objects.filter(email=data['email']).first()
        if user:
            user.set_password(data['new_password'])
            user.save()

        return Response(success_response(message='Password reset successfully.'))


class ChangePasswordView(APIView):
    """Change password for authenticated user."""
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response(success_response(message='Password changed successfully.'))


class EmailVerifyView(APIView):
    """Verify email address with OTP."""
    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = OTPVerification.objects.filter(
            user=request.user,
            otp_code=serializer.validated_data['otp_code'],
            purpose='verify_email',
            is_used=False,
        ).order_by('-created_at').first()

        if not otp or not otp.is_valid():
            return Response(
                {'success': False, 'error': {'message': 'Invalid or expired verification code.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.is_used = True
        otp.save()
        request.user.is_email_verified = True
        request.user.save(update_fields=['is_email_verified'])

        return Response(success_response(message='Email verified successfully.'))


# ==================================================
# User Profile & Settings Views
# ==================================================

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the authenticated user's profile."""
    serializer_class = UserDetailSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(success_response(data=serializer.data, message='Profile details'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(success_response(data=serializer.data, message='Profile updated successfully'))


class UserSettingsView(generics.RetrieveUpdateAPIView):
    """Get or update user settings/preferences."""
    serializer_class = UserSettingsSerializer

    def get_object(self):
        return self.request.user.profile

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(success_response(data=serializer.data, message='User settings'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(success_response(data=serializer.data, message='Settings updated successfully'))


class UserDeviceListView(generics.ListAPIView):
    """List all active device sessions."""
    serializer_class = UserDeviceSerializer
    pagination_class = None

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user, is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(success_response(data=serializer.data, message='Active devices list'))


class UserDeviceDeleteView(generics.DestroyAPIView):
    """Deactivate a device session."""
    serializer_class = UserDeviceSerializer

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(success_response(message='Device session revoked successfully'))


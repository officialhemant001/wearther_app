"""
Authentication URL patterns.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import (
    SignupView, LoginView, LogoutView,
    OTPRequestView, OTPVerifyView, GoogleAuthView,
    PasswordResetRequestView, PasswordResetConfirmView,
    ChangePasswordView, EmailVerifyView,
)

app_name = 'auth'

urlpatterns = [
    # JWT Auth
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # OTP
    path('otp/request/', OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify/', OTPVerifyView.as_view(), name='otp-verify'),

    # Google OAuth
    path('google/', GoogleAuthView.as_view(), name='google-auth'),

    # Password
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='password-change'),

    # Email verification
    path('email/verify/', EmailVerifyView.as_view(), name='email-verify'),
]

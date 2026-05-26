from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserDevice, OTPVerification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['email', 'username', 'is_email_verified', 'auth_provider', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_email_verified', 'auth_provider', 'is_staff']
    search_fields = ['email', 'username', 'phone_number']
    ordering = ['-created_at']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'is_email_verified', 'is_phone_verified', 'auth_provider', 'last_login_ip')}),
    )


@admin.register(UserDevice)
class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_name', 'device_type', 'ip_address', 'is_active', 'last_active']
    list_filter = ['device_type', 'is_active']


@admin.register(OTPVerification)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'phone_number', 'purpose', 'is_used', 'expires_at']
    list_filter = ['purpose', 'is_used']

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, OTP


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = ['email', 'email_verified_badge', 'is_staff_badge', 'date_joined', 'last_login']
    list_filter = ['email_verified', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email']
    ordering = ['-date_joined']
    
    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),
        ('Verification', {
            'fields': ('email_verified',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'email_verified'),
        }),
    )
    
    def email_verified_badge(self, obj):
        if obj.email_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        return format_html('<span style="color: red;">✗ Not Verified</span>')
    email_verified_badge.short_description = 'Email Status'
    
    def is_staff_badge(self, obj):
        if obj.is_staff:
            return format_html('<span style="color: blue;">Staff</span>')
        return format_html('<span style="color: gray;">User</span>')
    is_staff_badge.short_description = 'Role'


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """OTP management"""
    list_display = ['user', 'code', 'purpose', 'is_used_badge', 'expires_at', 'created_at']
    list_filter = ['purpose', 'is_used', 'created_at']
    search_fields = ['user__email', 'code']
    readonly_fields = ['user', 'code', 'purpose', 'expires_at', 'created_at']
    ordering = ['-created_at']
    
    def is_used_badge(self, obj):
        if obj.is_used:
            return format_html('<span style="color: gray;">Used</span>')
        return format_html('<span style="color: green;">Active</span>')
    is_used_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False  # Can't manually create OTPs

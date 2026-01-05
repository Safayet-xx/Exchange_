from django.contrib import admin
from django.utils.html import format_html
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile management"""
    list_display = ['user_email', 'display_name', 'handle', 'university', 'role_badge', 'is_completed_badge']
    list_filter = ['is_completed', 'role', 'university']
    search_fields = ['user__email', 'display_name', 'handle', 'full_name']
    readonly_fields = ['user']
    ordering = ['-id']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Basic Info', {
            'fields': ('display_name', 'full_name', 'handle', 'role')
        }),
        ('Contact', {
            'fields': ('phone_number',)
        }),
        ('Academic', {
            'fields': ('university', 'student_id')
        }),
        ('About', {
            'fields': ('bio', 'hobbies', 'fun_fact')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def role_badge(self, obj):
        if obj.role == 'professor':
            return format_html('<span style="color: blue;">👨‍🏫 Professor</span>')
        return format_html('<span style="color: green;">🎓 Student</span>')
    role_badge.short_description = 'Role'
    
    def is_completed_badge(self, obj):
        if obj.is_completed:
            return format_html('<span style="color: green;">✓ Complete</span>')
        return format_html('<span style="color: orange;">⚠ Incomplete</span>')
    is_completed_badge.short_description = 'Profile Status'

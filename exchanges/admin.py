from django.contrib import admin
from django.utils.html import format_html
from .models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Session management"""
    list_display = ['title', 'requester_email', 'helper_email', 'status_badge', 'credits', 'created_at']
    list_filter = ['status', 'level', 'created_at']
    search_fields = ['title', 'requester__email', 'helper__email']
    readonly_fields = ['requester', 'helper', 'agreed_amount', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Participants', {
            'fields': ('requester', 'helper')
        }),
        ('Session Details', {
            'fields': ('title', 'description', 'duration', 'level')
        }),
        ('Status & Credits', {
            'fields': ('status', 'agreed_amount')
        }),
        ('Timestamps', {
            'fields': ('scheduled_time', 'created_at', 'updated_at')
        }),
    )
    
    def requester_email(self, obj):
        return obj.requester.email
    requester_email.short_description = 'Requester'
    
    def helper_email(self, obj):
        return obj.helper.email
    helper_email.short_description = 'Helper'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'accepted': 'blue',
            'completed': 'green',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.status.upper()
        )
    status_badge.short_description = 'Status'
    
    def credits(self, obj):
        return format_html('<strong>{} credits</strong>', obj.agreed_amount)
    credits.short_description = 'Credits'

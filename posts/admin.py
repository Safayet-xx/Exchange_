from django.contrib import admin
from django.utils.html import format_html
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post management"""
    list_display = ['title', 'user_email', 'kind_badge', 'is_active_badge', 'created_at']
    list_filter = ['kind', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'user__email', 'skill_name']
    readonly_fields = ['user', 'created_at', 'updated_at', 'views']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Post Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Type & Skill', {
            'fields': ('kind', 'skill_name')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Stats', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def kind_badge(self, obj):
        if obj.kind == 'offer':
            return format_html('<span style="color: green;">🎁 Offering</span>')
        return format_html('<span style="color: blue;">🔍 Looking For</span>')
    kind_badge.short_description = 'Type'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: gray;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'

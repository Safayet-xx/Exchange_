from django.contrib import admin
from django.utils.html import format_html
from .models import SkillCategory, Skill, UserSkill


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    """Skill category management"""
    list_display = ['name', 'icon']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Skill management"""
    list_display = ['name', 'category', 'user_count']
    list_filter = ['category']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def user_count(self, obj):
        count = obj.user_skills.count()
        return format_html('<span style="color: blue;">{} users</span>', count)
    user_count.short_description = 'Users with this skill'


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    """User skill management"""
    list_display = ['user_email', 'skill', 'department', 'proficiency_badge', 'experience', 'created_at']
    list_filter = ['department', 'proficiency_level', 'created_at']
    search_fields = ['user__email', 'skill__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User & Skill', {
            'fields': ('user', 'skill')
        }),
        ('Details', {
            'fields': ('department', 'proficiency_level', 'years_of_experience', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def proficiency_badge(self, obj):
        colors = {
            'beginner': 'orange',
            'intermediate': 'blue',
            'advanced': 'green',
            'expert': 'purple'
        }
        color = colors.get(obj.proficiency_level, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_proficiency_level_display()
        )
    proficiency_badge.short_description = 'Proficiency'
    
    def experience(self, obj):
        return f"{obj.years_of_experience} years"
    experience.short_description = 'Experience'

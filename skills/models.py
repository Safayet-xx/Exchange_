from django.db import models
from django.conf import settings


class SkillCategory(models.Model):
    """Categories for organizing skills"""
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')
    
    class Meta:
        ordering = ['name']
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual skills that users can have"""
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='skills')
    description = models.TextField(blank=True, default='')
    
    class Meta:
        ordering = ['name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """Skills that a user has - shown on their profile"""
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner (0-1 years)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3-5 years)'),
        ('expert', 'Expert (5+ years)'),
    ]
    
    DEPARTMENTS = [
        ('engineering', 'Engineering'),
        ('biomedical', 'Bio Medical'),
        ('commerce', 'Commerce and Finance'),
        ('fine_arts', 'Fine Arts'),
        ('computer_science', 'Computer Science'),
        ('mathematics', 'Mathematics and Statistics'),
        ('physics', 'Physics and Astronomy'),
        ('chemistry', 'Chemistry'),
        ('biological', 'Biological Sciences'),
        ('law', 'Law'),
        ('psychology', 'Psychology'),
        ('history', 'History'),
        ('politics', 'Politics and International Relations'),
        ('english', 'English Language and Literature'),
        ('medicine', 'Medicine'),
        ('nursing', 'Nursing and Midwifery'),
        ('architecture', 'Architecture'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="user_skills")
    department = models.CharField(max_length=50, choices=DEPARTMENTS, default='other', help_text="Your academic department")
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='beginner')
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    description = models.TextField(blank=True, default='', help_text="Describe your experience with this skill")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [('user', 'skill')]
        ordering = ['-years_of_experience', 'skill__name']
        verbose_name = "User Skill"
        verbose_name_plural = "User Skills"
    
    def __str__(self):
        return f"{self.user.email} - {self.skill.name} ({self.proficiency_level})"

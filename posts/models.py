from django.db import models
from django.conf import settings


class Post(models.Model):
    """Posts for offering or requesting help - Marketplace"""
    KIND_CHOICES = [
        ('offer', 'Offering Help'),
        ('want', 'Looking for Help'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    title = models.CharField(max_length=150)
    description = models.TextField()
    skill_name = models.CharField(max_length=100, help_text="What skill is this about?")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
    
    def __str__(self):
        return f"{self.user.email} - {self.get_kind_display()}: {self.title}"

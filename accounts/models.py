from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.conf import settings
from datetime import timedelta
import random


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model using email instead of username."""
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class OTP(models.Model):
    """Model for handling OTPs (signup, login, password reset)."""
    PURPOSES = (
        ("signup", "Sign Up"),
        ("login", "Login"),
        ("reset", "Password Reset"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps"
    )
    code = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^\d{6}$", "OTP must be 6 digits")]
    )
    purpose = models.CharField(max_length=12, choices=PURPOSES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    last_sent = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "purpose", "is_used", "expires_at"]),
        ]

    @classmethod
    def issue(cls, user, purpose="signup", length=6, ttl_minutes=10):
        """Issue a new OTP and invalidate previous unused ones for this purpose."""
        cls.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)
        code = "".join(str(random.randint(0, 9)) for _ in range(length))
        now = timezone.now()
        return cls.objects.create(
            user=user,
            code=code,
            purpose=purpose,
            expires_at=now + timedelta(minutes=ttl_minutes),
        )

    def is_valid(self, code):
        """Check if the given code matches and is not expired/used."""
        return (
            not self.is_used
            and timezone.now() <= self.expires_at
            and self.code == code
        )

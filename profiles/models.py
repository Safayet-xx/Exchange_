from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("professor", "Professor"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Role-based access
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    # Public bits
    full_name = models.CharField(max_length=120, blank=True)
    handle = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    display_name = models.CharField(max_length=80, blank=True)

    # Extended profile fields
    bio = models.TextField(blank=True)
    university = models.CharField(max_length=255, blank=True)
    joined_date = models.DateField(blank=True, null=True)
    hobbies = models.CharField(max_length=255, blank=True)
    fun_fact = models.CharField(max_length=255, blank=True)

    # Flow flags
    email_verified = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name or self.full_name or getattr(self.user, "email", str(self.user))

    @property
    def average_rating(self):
        """Average rating from professors (if the user is a student)."""
        endorsements = self.user.endorsements_received.all()
        if endorsements.exists():
            return round(sum(e.rating for e in endorsements) / endorsements.count(), 2)
        return None

    @property
    def rating_count(self):
        """Number of endorsements received."""
        return self.user.endorsements_received.count()


class Endorsement(models.Model):
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="endorsements_given",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="endorsements_received",
    )
    rating = models.PositiveSmallIntegerField()  # 1–5 scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("professor", "student")]

    def __str__(self):
        return f"{self.professor} → {self.student} ({self.rating}/5)"

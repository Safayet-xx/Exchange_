from django.conf import settings
from django.db import models, transaction
from django.core.exceptions import ValidationError

class Session(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
    
    class Duration(models.TextChoices):
        SIXTY = "60", "60 minutes"
        NINETY = "90", "90 minutes"
        TWOHOURS = "120", "2 hours"
    
    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions_requested"
    )
    helper = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions_helping"
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    
    # Auto-calculated credit system
    duration = models.CharField(max_length=10, choices=Duration.choices, default=Duration.SIXTY)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    agreed_amount = models.PositiveIntegerField(default=1)
    
    # Scheduling
    scheduled_time = models.DateTimeField(null=True, blank=True, help_text="When the session is scheduled")
    
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    credits_transferred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Credit calculation table
    CREDIT_TABLE = {
        ('60', 'beginner'): 5,
        ('60', 'intermediate'): 7,
        ('60', 'advanced'): 9,
        ('90', 'beginner'): 7,
        ('90', 'intermediate'): 9,
        ('90', 'advanced'): 12,
        ('120', 'beginner'): 10,
        ('120', 'intermediate'): 12,
        ('120', 'advanced'): 15,
    }
    
    def calculate_credits(self):
        """Auto-calculate credits based on duration and level"""
        return self.CREDIT_TABLE.get((self.duration, self.level), 5)
    
    def save(self, *args, **kwargs):
        # Auto-calculate credits before saving
        self.agreed_amount = self.calculate_credits()
        super().save(*args, **kwargs)

    def clean(self):
        if self.requester_id == self.helper_id:
            raise ValidationError("Requester and helper must be different users.")
        if self.agreed_amount <= 0:
            raise ValidationError("Agreed amount must be positive.")

    def mark_completed(self, by_user):
        from credits.models import transfer_credits
        if by_user != self.requester and not getattr(by_user, "is_staff", False):
            raise ValidationError("Only the requester (or staff) can mark a session completed.")
        with transaction.atomic():
            sess = Session.objects.select_for_update().get(pk=self.pk)
            if sess.status == Session.Status.COMPLETED:
                return sess
            if sess.status not in (Session.Status.ACCEPTED, Session.Status.PENDING):
                raise ValidationError(f"Cannot complete a session in status '{sess.status}'.")
            sess.status = Session.Status.COMPLETED
            sess.save(update_fields=["status", "updated_at"])
            if not sess.credits_transferred:
                transfer_credits(
                    from_user=sess.requester, to_user=sess.helper,
                    amount=sess.agreed_amount, note=f"Session #{sess.id}", session=sess
                )
                sess.credits_transferred = True
                sess.save(update_fields=["credits_transferred", "updated_at"])
        return sess

    def __str__(self):
        return f"Session #{self.pk} {self.requester} → {self.helper} ({self.status})"

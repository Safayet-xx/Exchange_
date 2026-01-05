"""
Signals for automatic wallet creation when a user is created
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CreditWallet

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet_for_user(sender, instance, created, **kwargs):
    """
    Automatically create a credit wallet when a new user is created
    """
    if created:
        CreditWallet.objects.get_or_create(
            user=instance,
            defaults={'balance': settings.INITIAL_CREDITS}
        )

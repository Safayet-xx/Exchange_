
from django.apps import AppConfig

class CreditsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "credits"

    def ready(self):
        from django.db.models.signals import post_save
        from django.conf import settings
        from .models import CreditWallet
        from django.dispatch import receiver

        @receiver(post_save, sender=settings.AUTH_USER_MODEL)
        def create_wallet(sender, instance, created, **kwargs):
            if created:
                CreditWallet.objects.get_or_create(user=instance)

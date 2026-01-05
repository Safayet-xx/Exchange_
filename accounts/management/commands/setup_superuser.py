from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Profile
from credits.models import CreditWallet

User = get_user_model()


class Command(BaseCommand):
    help = 'Setup profile and wallet for superusers'

    def handle(self, *args, **kwargs):
        superusers = User.objects.filter(is_superuser=True)
        
        for user in superusers:
            # Create profile if doesn't exist
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'display_name': 'Admin',
                    'full_name': 'System Administrator',
                    'handle': user.email.split('@')[0],
                    'university': 'System',
                    'bio': 'Platform Administrator',
                    'is_completed': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created profile for {user.email}')
                )
            
            # Make sure user is verified
            if not user.email_verified:
                user.email_verified = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Verified email for {user.email}')
                )
            
            # Create wallet if doesn't exist
            wallet, created = CreditWallet.objects.get_or_create(
                user=user,
                defaults={'balance': 100}  # Give admin 100 credits
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created wallet for {user.email} with 100 credits')
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'\n✓ Superuser {user.email} is ready to use the platform!')
            )

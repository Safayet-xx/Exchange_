from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class SuperuserAutoVerifyBackend(ModelBackend):
    """
    Custom authentication backend that auto-verifies superusers
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate and auto-verify superusers"""
        try:
            # Try to get user
            user = User.objects.get(email=username)
            
            # Check password
            if user.check_password(password):
                # If superuser or staff, auto-verify email
                if user.is_superuser or user.is_staff:
                    if not user.email_verified:
                        user.email_verified = True
                        user.save()
                
                return user
        except User.DoesNotExist:
            return None
        
        return None

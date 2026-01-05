from django.shortcuts import redirect
from django.urls import resolve, reverse

class ProfileCompletionMiddleware:
    """
    Enforce profile completion flow for authenticated users.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that are always accessible
        self.exempt_paths = [
            '/static/',
            '/media/',
            '/admin/',
        ]
        
        # URL names that don't require completed profile
        self.exempt_names = {
            'accounts:login',
            'accounts:logout',
            'accounts:signup',
            'accounts:verify_otp',
            'accounts:resend_otp',
            'profiles:setup',
        }

    def __call__(self, request):
        path = request.path
        
        # Allow exempt paths (static, media, admin)
        for exempt_path in self.exempt_paths:
            if path.startswith(exempt_path):
                return self.get_response(request)
        
        # Only check authenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Get current URL name
        try:
            match = resolve(path)
            current_name = f"{match.namespace}:{match.url_name}" if match.namespace else match.url_name
        except:
            current_name = None
        
        # Allow exempt URL names
        if current_name in self.exempt_names:
            return self.get_response(request)
        
        # Check if email is verified (on User model)
        if not request.user.email_verified:
            # Not verified, redirect to OTP page
            if current_name != 'accounts:verify_otp':
                return redirect('accounts:verify_otp')
            return self.get_response(request)
        
        # Email is verified, check if profile is complete
        try:
            profile = request.user.profile
            if not profile.is_completed:
                # Profile not complete, redirect to setup
                if current_name != 'profiles:setup':
                    return redirect('profiles:setup')
        except:
            # No profile exists, redirect to setup
            if current_name != 'profiles:setup':
                return redirect('profiles:setup')
        
        # Everything is good, proceed
        return self.get_response(request)

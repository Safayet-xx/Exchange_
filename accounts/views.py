"""
Authentication views with OTP email verification
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import os
import random  # ✅ added

from .models import User, OTP
from .forms import SignUpForm


# ✅ added (needed by unit tests)
def generate_otp_code():
    """Return a 6-digit numeric OTP as a string (used by unit tests)."""
    return f"{random.randint(100000, 999999)}"


# ✅ added (needed by unit tests)
def is_otp_expired(created_at, expiry_minutes=10):
    """Return True if created_at is older than expiry_minutes (used by unit tests)."""
    return timezone.now() > created_at + timedelta(minutes=expiry_minutes)


def signup_view(request):
    """
    Handle user registration with university email validation.
    Creates user account and sends OTP for email verification.
    """
    # If user is already logged in and verified, redirect to home
    if request.user.is_authenticated:
        if request.user.email_verified:
            try:
                if request.user.profile.is_completed:
                    messages.info(request, "You are already logged in.")
                    return redirect('core:home')
            except:
                pass
        # If authenticated but not verified, go to OTP
        return redirect('accounts:verify_otp')
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create user but don't log them in yet
            user = form.save(commit=False)
            user.email_verified = False
            user.save()
            
            # Generate OTP
            otp = OTP.issue(
                user=user,
                purpose='signup',
                length=settings.OTP_CODE_LENGTH,
                ttl_minutes=settings.OTP_EXP_MINUTES
            )
            
            # Send OTP email
            try:
                if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
                    send_mail(
                        subject='Verify Your Email - Exchange Platform',
                        message=f'Your verification code is: {otp.code}\n\nThis code will expire in {settings.OTP_EXP_MINUTES} minutes.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    messages.success(request, f"Verification code sent to {user.email}")
                else:
                    # Console backend for development
                    messages.success(request, f"Verification code: {otp.code} (check console)")
                    print(f"\n{'='*60}\nOTP: {otp.code}\nFor: {user.email}\n{'='*60}\n")
            except Exception as e:
                messages.warning(request, f"Email sending failed. OTP: {otp.code} (Save this!)")
                print(f"Email error: {e}")
                print(f"OTP for {user.email}: {otp.code}")
            
            # Log user in (but still need to verify)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:verify_otp')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def verify_otp_view(request):
    """
    Verify the OTP code sent to user's email.
    """
    user = request.user
    
    # If already verified, redirect
    if user.email_verified:
        try:
            if user.profile.is_completed:
                messages.success(request, "Email already verified!")
                return redirect('core:home')
        except:
            pass
        return redirect('profiles:setup')
    
    if request.method == "POST":
        code = request.POST.get('code', '').strip()
        
        if not code:
            messages.error(request, "Please enter the verification code.")
            return render(request, 'accounts/verify_otp.html')
        
        # Get the most recent OTP for this user
        otp = OTP.objects.filter(
            user=user,
            purpose='signup',
            is_used=False
        ).order_by('-created_at').first()
        
        if not otp:
            messages.error(request, "No verification code found. Please request a new one.")
            return render(request, 'accounts/verify_otp.html')
        
        # Validate the OTP
        if not otp.is_valid(code):
            messages.error(request, "Invalid or expired code. Please try again.")
            return render(request, 'accounts/verify_otp.html')
        
        # Mark OTP as used
        otp.is_used = True
        otp.save()
        
        # Mark user as verified
        user.email_verified = True
        user.save()
        
        messages.success(request, "Email verified successfully!")
        
        # Check if profile exists and is complete
        try:
            if user.profile.is_completed:
                return redirect('core:home')
        except:
            pass
        
        return redirect('profiles:setup')
    
    return render(request, 'accounts/verify_otp.html')


@login_required
def resend_otp_view(request):
    """
    Resend OTP to user's email.
    """
    user = request.user
    
    if user.email_verified:
        messages.info(request, "Your email is already verified.")
        return redirect('core:home')
    
    # Generate new OTP
    otp = OTP.issue(
        user=user,
        purpose='signup',
        length=settings.OTP_CODE_LENGTH,
        ttl_minutes=settings.OTP_EXP_MINUTES
    )
    
    # Send OTP email
    try:
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
            send_mail(
                subject='Verify Your Email - Exchange Platform',
                message=f'Your verification code is: {otp.code}\n\nThis code will expire in {settings.OTP_EXP_MINUTES} minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            messages.success(request, "New verification code sent to your email!")
        else:
            messages.success(request, f"New verification code: {otp.code}")
            print(f"\n{'='*60}\nOTP: {otp.code}\nFor: {user.email}\n{'='*60}\n")
    except Exception as e:
        messages.warning(request, f"Email sending failed. OTP: {otp.code}")
        print(f"Email error: {e}")
        print(f"OTP for {user.email}: {otp.code}")
    
    return redirect('accounts:verify_otp')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('core:home')


def forgot_password_view(request):
    """
    Request password reset - send OTP to email
    """
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, 'accounts/forgot_password.html')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate OTP for password reset
            otp = OTP.issue(
                user=user,
                purpose='password_reset',
                length=settings.OTP_CODE_LENGTH,
                ttl_minutes=settings.OTP_EXP_MINUTES
            )
            
            # Send OTP email
            try:
                if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
                    send_mail(
                        subject='Password Reset - Exchange Platform',
                        message=f'Your password reset code is: {otp.code}\n\nThis code will expire in {settings.OTP_EXP_MINUTES} minutes.\n\nIf you did not request this, please ignore this email.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    messages.success(request, f"Password reset code sent to {email}")
                else:
                    # Console backend for development
                    messages.success(request, f"Password reset code: {otp.code} (check console)")
                    print(f"\n{'='*60}\nPASSWORD RESET OTP: {otp.code}\nFor: {email}\n{'='*60}\n")
            except Exception as e:
                messages.warning(request, f"Email sending failed. OTP: {otp.code} (Save this!)")
                print(f"Email error: {e}")
                print(f"Password reset OTP for {email}: {otp.code}")
            
            # Store email in session for OTP verification
            request.session['reset_email'] = email
            return redirect('accounts:reset_verify_otp')
            
        except User.DoesNotExist:
            # Don't reveal if email exists or not (security)
            messages.success(request, f"If {email} exists, a password reset code has been sent.")
            return render(request, 'accounts/forgot_password.html')
    
    return render(request, 'accounts/forgot_password.html')


def reset_verify_otp_view(request):
    """
    Verify OTP for password reset
    """
    reset_email = request.session.get('reset_email')
    
    if not reset_email:
        messages.error(request, "Please start the password reset process first.")
        return redirect('accounts:forgot_password')
    
    if request.method == "POST":
        code = request.POST.get('code', '').strip()
        
        if not code:
            messages.error(request, "Please enter the verification code.")
            return render(request, 'accounts/reset_verify_otp.html', {'email': reset_email})
        
        try:
            user = User.objects.get(email=reset_email)
            
            # Get the most recent unused OTP for password reset
            otp = OTP.objects.filter(
                user=user,
                purpose='password_reset',
                is_used=False
            ).order_by('-created_at').first()
            
            if not otp:
                messages.error(request, "No valid reset code found. Please request a new one.")
                return redirect('accounts:forgot_password')
            
            # Validate the OTP with the provided code
            if not otp.is_valid(code):
                messages.error(request, "Invalid or expired code. Please try again or request a new code.")
                return render(request, 'accounts/reset_verify_otp.html', {'email': reset_email})
            
            # Mark OTP as used
            otp.is_used = True
            otp.save()
            
            # Store verification in session
            request.session['reset_verified'] = True
            request.session['reset_user_id'] = user.id
            
            messages.success(request, "Code verified! Please set your new password.")
            return redirect('accounts:reset_password')
            
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('accounts:forgot_password')
    
    return render(request, 'accounts/reset_verify_otp.html', {'email': reset_email})


def reset_password_view(request):
    """
    Set new password after OTP verification
    """
    if not request.session.get('reset_verified'):
        messages.error(request, "Please verify your email first.")
        return redirect('accounts:forgot_password')
    
    user_id = request.session.get('reset_user_id')
    
    if request.method == "POST":
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        
        if not password1 or not password2:
            messages.error(request, "Please enter both password fields.")
            return render(request, 'accounts/reset_password.html')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/reset_password.html')
        
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, 'accounts/reset_password.html')
        
        try:
            user = User.objects.get(id=user_id)
            user.set_password(password1)
            user.save()
            
            # Clear session data
            request.session.pop('reset_email', None)
            request.session.pop('reset_verified', None)
            request.session.pop('reset_user_id', None)
            
            messages.success(request, "Password reset successful! You can now login with your new password.")
            return redirect('accounts:login')
            
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('accounts:forgot_password')
    
    return render(request, 'accounts/reset_password.html')

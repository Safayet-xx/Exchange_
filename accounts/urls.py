from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Registration & Verification
    path("signup/", views.signup_view, name="signup"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("resend-otp/", views.resend_otp_view, name="resend_otp"),
    
    # Password Reset
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("reset-verify-otp/", views.reset_verify_otp_view, name="reset_verify_otp"),
    path("reset-password/", views.reset_password_view, name="reset_password"),
]

"""
Django settings for Exchange Platform.
University Skill Exchange Platform - Complete Configuration
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-frfdk+5u4frux4by)5^x73lb8b79bmrt7rnwa2pn*xj4di!fa8')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,*').split(',')

# Stytch Configuration
STYTCH_PROJECT_ID = os.getenv('STYTCH_PROJECT_ID')
STYTCH_SECRET = os.getenv('STYTCH_SECRET')
STYTCH_PUBLIC_TOKEN = os.getenv('STYTCH_PUBLIC_TOKEN')
STYTCH_PROJECT_DOMAIN = os.getenv('STYTCH_PROJECT_DOMAIN')
STYTCH_ENVIRONMENT = os.getenv('STYTCH_ENVIRONMENT', 'test')

# Application definition
INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps

    # Project apps
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "posts",  # Posts - Marketplace
    "skills.apps.SkillsConfig",  # Skills - Profile expertise
    "profiles.apps.ProfilesConfig",
    "credits.apps.CreditsConfig",
    "exchanges.apps.ExchangesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "accounts.middleware.ProfileCompletionMiddleware",  # Custom middleware
]

ROOT_URLCONF = "exchange.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "exchange.wsgi.application"

# Database
# Database
# Default: SQLite for local/dev. For Docker/production set DB_ENGINE=postgres (or provide DB_* vars).
DB_ENGINE = os.getenv("DB_ENGINE", "").lower()

USE_POSTGRES = DB_ENGINE in {"postgres", "postgresql"} or os.getenv("POSTGRES_DB") or os.getenv("DB_HOST")

if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "exchange")),
            "USER": os.getenv("DB_USER", os.getenv("POSTGRES_USER", "exchange")),
            "PASSWORD": os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD", "exchange")),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

# WhiteNoise: serve static files directly from the app
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (User uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============ Custom Authentication Settings ============
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

# Custom authentication backend (auto-verifies superusers)
AUTHENTICATION_BACKENDS = [
    'accounts.backends.SuperuserAutoVerifyBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ============ OTP & Email Verification ============
OTP_CODE_LENGTH = 6
OTP_EXP_MINUTES = 10
OTP_RESEND_COOLDOWN_S = 60
ALLOWED_UNI_DOMAINS = {
    "surrey.ac.uk", 
    "brunel.ac.uk", 
    "imperial.ac.uk", 
    "ucl.ac.uk",
    "example.edu",  # Add more universities as needed
}

# Email settings
# Using environment variables for email configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')  # Your Gmail address
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')  # App password
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Exchange Platform <noreply@exchange-platform.com>')

# For development, you can use console backend
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ============ REST Framework Settings ============

# ============ CORS Settings for React Frontend ============
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# ============ Credit System Settings ============
INITIAL_CREDITS = 10  # Credits given to new users

# ============ Admin Panel Settings ============
ADMIN_URL = "admin/"  # Change to something secret in production



# ============ Stytch Authentication Settings ============
# These values are used by accounts/utils_stytch.py for email OTP via Stytch.
# In production you would normally load these from environment variables.
STYTCH_PROJECT_ID = "project-test-a6dc714f-06d9-4dc8-b263-076a9b14f280"
STYTCH_SECRET = "secret-test-IWS1hpu4MXrjRIRW5AZcDjJIeNzC_EUb--o="
STYTCH_PUBLIC_TOKEN = "public-token-test-29a09886-d85b-4152-bdbd-adc8b683cd81"
# Use 'test' for your Stytch test project, 'live' for live.
STYTCH_ENV = "test"

# ============ Security Settings (Enhance for production) ============
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

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
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-frfdk+5u4frux4by)5^x73lb8b79bmrt7rnwa2pn*xj4di!fa8",
)
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Stytch Configuration (from env only)
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
STYTCH_PUBLIC_TOKEN = os.getenv("STYTCH_PUBLIC_TOKEN")
STYTCH_PROJECT_DOMAIN = os.getenv("STYTCH_PROJECT_DOMAIN")
STYTCH_ENVIRONMENT = os.getenv("STYTCH_ENVIRONMENT", "test")

# Application definition
INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps (add here if needed)

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
    "accounts.backends.SuperuserAutoVerifyBackend",
    "django.contrib.auth.backends.ModelBackend",
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

# ===================== EMAIL SETTINGS =====================
# Robust parsing of env vars and safe defaults.
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))

EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() in ("true", "1", "yes")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# IMPORTANT: if DEFAULT_FROM_EMAIL isn't set correctly, fallback to EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL") or EMAIL_HOST_USER or "noreply@localhost"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ===================== CORS (if you use django-cors-headers) =====================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# ============ Credit System Settings ============
INITIAL_CREDITS = 10  # Credits given to new users

# ============ Admin Panel Settings ============
ADMIN_URL = "admin/"  # Change to something secret in production

# ============ Security Settings (Enhance for production) ============
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

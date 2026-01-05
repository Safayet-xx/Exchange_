

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables (optional; Docker does NOT require .env)
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# Core Security / Runtime
# =========================================================
# NOTE: For production you MUST set SECRET_KEY via environment variable.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-me-in-production",
)

# Robust DEBUG parsing (accepts 1/0, true/false, yes/no)
DEBUG = os.getenv("DEBUG", "1") in {"1", "true", "True", "yes", "YES"}

# Allowed hosts (supports either DJANGO_ALLOWED_HOSTS or ALLOWED_HOSTS)
_hosts_raw = os.getenv("DJANGO_ALLOWED_HOSTS") or os.getenv(
    "ALLOWED_HOSTS", "localhost,127.0.0.1"
)
ALLOWED_HOSTS = [h.strip() for h in _hosts_raw.split(",") if h.strip()]

# =========================================================
# Stytch Configuration (NO hardcoded secrets)
# =========================================================
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID", "")
STYTCH_SECRET = os.getenv("STYTCH_SECRET", "")
STYTCH_PUBLIC_TOKEN = os.getenv("STYTCH_PUBLIC_TOKEN", "")
STYTCH_PROJECT_DOMAIN = os.getenv("STYTCH_PROJECT_DOMAIN", "")
STYTCH_ENVIRONMENT = os.getenv("STYTCH_ENVIRONMENT", "test")


# =========================================================
# Application definition
# =========================================================
INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps (add here if you use them, e.g., corsheaders)
    # "corsheaders",

    # Project apps
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    "posts",  # marketplace posts
    "skills.apps.SkillsConfig",
    "profiles.apps.ProfilesConfig",
    "credits.apps.CreditsConfig",
    "exchanges.apps.ExchangesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # If you enable corsheaders:
    # "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Custom middleware
    "accounts.middleware.ProfileCompletionMiddleware",
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


# =========================================================
# Database
# =========================================================
# Default: SQLite for local/dev.
# For Docker/production set DB_ENGINE=postgres (or provide DB_* vars).
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


# =========================================================
# Password validation
# =========================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =========================================================
# Internationalization
# =========================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# =========================================================
# Static files (CSS, JavaScript, Images)
# =========================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

# WhiteNoise: serve static files directly from the app
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================================================
# Media files (User uploads)
# =========================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# Default primary key field type
# =========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# Custom Authentication Settings
# =========================================================
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.SuperuserAutoVerifyBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# =========================================================
# OTP & Email Verification
# =========================================================
OTP_CODE_LENGTH = 6
OTP_EXP_MINUTES = 10
OTP_RESEND_COOLDOWN_S = 60

ALLOWED_UNI_DOMAINS = {
    "surrey.ac.uk",
    "brunel.ac.uk",
    "imperial.ac.uk",
    "ucl.ac.uk",
    "example.edu",
}


# =========================================================
# Email settings (env-controlled)
# =========================================================
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") in {"1", "true", "True", "yes", "YES"}
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Exchange Platform <noreply@exchange-platform.com>")

# For development you can switch to console backend by setting:
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend


# =========================================================
# CORS Settings (only if you enable django-cors-headers)
# =========================================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True


# =========================================================
# Credit System Settings
# =========================================================
INITIAL_CREDITS = int(os.getenv("INITIAL_CREDITS", "10"))


# =========================================================
# Admin Panel Settings
# =========================================================
ADMIN_URL = os.getenv("ADMIN_URL", "admin/")


# =========================================================
# Security & Deployment Settings (IMPORTANT for Docker)
# =========================================================
# Prevent the HTTP -> HTTPS redirect that was breaking localhost in Docker.
# Enable these ONLY if you're actually serving behind HTTPS.
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "0") in {"1", "true", "True", "yes", "YES"}
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") in {"1", "true", "True", "yes", "YES"}
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "0") in {"1", "true", "True", "yes", "YES"}

# CSRF Trusted Origins (optional; needed if you host behind HTTPS with a domain)
_csrf_raw = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_raw.split(",") if o.strip()]

# HSTS (enable only in real HTTPS production)
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "0") in {"1", "true", "True", "yes", "YES"}
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "0") in {"1", "true", "True", "yes", "YES"}

# Proxy SSL header (ONLY enable if using a reverse proxy that sets X-Forwarded-Proto)
USE_X_FORWARDED_HOST = os.getenv("USE_X_FORWARDED_HOST", "0") in {"1", "true", "True", "yes", "YES"}
SECURE_PROXY_SSL_HEADER = None
if os.getenv("USE_SECURE_PROXY_SSL_HEADER", "0") in {"1", "true", "True", "yes", "YES"}:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Extra safe defaults
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

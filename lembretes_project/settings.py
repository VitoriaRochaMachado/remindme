# lembretes_project/settings.py
import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------- BASIC / SECURITY ----------
# SECRET_KEY must come from env in production. If not provided in local dev, generate a random one.
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

# DEBUG should be False in production. In dev you can set DEBUG=True via env.
DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

# ALLOWED_HOSTS from env (comma-separated). Default allows localhost for dev.
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# ---------- APPLICATIONS ----------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "notes",  # seu app de notas
    # adicione outros apps aqui se tiver
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lembretes_project.urls"

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
                "notes.context_processors.in_app_notifications",  # in-app notifications
            ],
        },
    },
]

WSGI_APPLICATION = "lembretes_project.wsgi.application"

# ---------- DATABASE ----------
# By default use sqlite for dev. In production you can set DATABASE_URL (postgres).
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------- PASSWORD VALIDATION ----------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------- INTERNATIONALIZATION ----------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ---------- STATIC FILES ----------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic writes here (Render)
STATICFILES_DIRS = [BASE_DIR / "static"]

# ---------- MEDIA (se usar) ----------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------- EMAIL (via env) ----------
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", os.getenv("EMAIL_HOST_USER", "no-reply@remindme.local"))
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# ---------- SECURITY / HTTPS (produção) ----------
# Só habilite SECURE_SSL_REDIRECT se seu domínio estiver servindo via HTTPS (Render já usa)
FORCE_SSL = os.getenv("FORCE_SSL", "True").lower() in ("1", "true", "yes")
SESSION_COOKIE_SECURE = not DEBUG and FORCE_SSL
CSRF_COOKIE_SECURE = not DEBUG and FORCE_SSL
SECURE_SSL_REDIRECT = not DEBUG and FORCE_SSL
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# ---------- LOGGING (console for Render) ----------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# ---------- AUTHENTICATION Redirects ----------
LOGIN_REDIRECT_URL = "notes:home"
LOGOUT_REDIRECT_URL = "login"
LOGIN_URL = "login"

# ---------- EXTRA / DEFAULTS ----------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------- OPTIONAL: django-crontab / django-crontasks ----------
# NOTE: If you plan to use Render Cron jobs, you don't need django-crontab.
# If you still use django-crontab locally, keep the lines below commented or remove them:
# CRONJOBS = [
#     ('*/5 * * * *', 'django.core.management.call_command', ['send_reminders']),
# ]

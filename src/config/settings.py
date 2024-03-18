"""Django settings for movie-recommender project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

from decouple import Config, RepositoryEnv, config  # type: ignore[import-untyped]
from dj_database_url import parse as db_url
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = config
if config("READ_DOT_ENV_FILE", default=True, cast=bool):
    env = Config(RepositoryEnv(BASE_DIR / ".env"))


# Admins
ADMINS = ["William Fernandes <william.winchester1967@gmail.com>"]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


# Hosting policy

ALLOWED_HOSTS = env(
    "ALLOWED_HOSTS", default=["*"], cast=lambda v: [s.strip() for s in v.split(",")]
)

INTERNAL_IPS = [
    "127.0.0.1",
]
if env("USE_DOCKER", default=False, cast=bool):
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
]

THIRD_PARTY_APPS: list[str] = [
    "django_celery_beat",
    "django_filters",
    "django_celery_results",
    "rest_framework",
    "rest_framework_simplejwt",
    "anymail",
] + (["debug_toolbar"] if DEBUG else [])

LOCAL_APPS: list[str] = ["users", "addresses", "hotels", "bookings"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
] + (["debug_toolbar.middleware.DebugToolbarMiddleware"] if DEBUG else [])


ROOT_URLCONF = "config.urls"


SITE_ID = 1


# Email

EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if DEBUG
    else "anymail.backends.sendgrid.EmailBackend"
)

EMAIL_HOST = env("EMAIL_HOST", default="mailpit")

SERVER_EMAIL = env("SERVER_EMAIL", default="root@localhost")

EMAIL_PORT = 1025

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="bookings@bix.com")

ANYMAIL = {
    "SENDGRID_API_KEY": env("SENDGRID_API_KEY", default=""),
    "SENDGRID_API_URL": env("SENDGRID_API_URL", default="https://api.sendgrid.com/v3/"),
}


# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# Messages

MESSAGE_TAGS = {message_constants.ERROR: "danger"}


# WSGI configuration.

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": env(
        "DATABASE_URL", default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', cast=db_url
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Authentication

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-use"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

PHONENUMBER_DEFAULT_REGION = "BR"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Celery

CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BEAT_SCHEDULE = {
    "cancel_unchecked_bookings_every_1_hour": {
        "task": "bookings.tasks.cancel_unchecked_bookings",
        "schedule": 60 * 60,
    },
    "retry_send_confirmation_email_for_pending_bookings_every_5_minutes": {
        "task": "retry_send_confirmation_email_for_pending_bookings",
        "schedule": 60 * 5,
    },
}


# Rest Framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
    + (["rest_framework.authentication.SessionAuthentication"] if DEBUG else []),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
}


# Bookings

BOOKINGS_CONFIRMATION_EMAIL_TEMPLATE_ID = env(
    "BOOKINGS_CONFIRMATION_EMAIL_TEMPLATE_ID", default=""
)

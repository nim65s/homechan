"""Django settings for homechan project."""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT = "homechan"
PROJECT_VERBOSE = "Home Channels"

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
if DEBUG:
    SECRET_KEY = "django-insecure-un&^-yd2(xdo#_@or@obzh)trtweg))^oegpor8@=$srjplaz1"
else:
    SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    PROJECT,
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "chat",
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

ROOT_URLCONF = f"{PROJECT}.urls"

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

WSGI_APPLICATION = f"{PROJECT}.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DB = os.environ.get("DB", "db.sqlite3")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / DB,
        "TEST": {
            "NAME": BASE_DIR / "db_test.sqlite3",
        },
    }
}
if DB == "postgres":
    DATABASES["default"].update(
        ENGINE="django.db.backends.postgresql",
        NAME=os.environ.get("POSTGRES_DB", DB),
        USER=os.environ.get("POSTGRES_USER", DB),
        HOST=os.environ.get("POSTGRES_HOST", DB),
        PASSWORD=os.environ["POSTGRES_PASSWORD"],
    )

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

_AUTH_PASSWORD_VALIDATORS = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{_AUTH_PASSWORD_VALIDATORS}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{_AUTH_PASSWORD_VALIDATORS}.MinimumLengthValidator",
    },
    {
        "NAME": f"{_AUTH_PASSWORD_VALIDATORS}.CommonPasswordValidator",
    },
    {
        "NAME": f"{_AUTH_PASSWORD_VALIDATORS}.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

MEDIA_ROOT = f"/srv/{PROJECT}/media/"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = f"/srv/{PROJECT}/static/"
LOGIN_REDIRECT_URL = "/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ASGI_APPLICATION = "homechan.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_HOST", "redis"), 6379)],
        },
    },
}

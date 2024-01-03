"""
Django settings for store project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import cloudinary
from decouple import config
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    "SECRET_KEY"
)  # "django-insecure-j1!-h4n#3&6=4*nxh(x-s6@zdveuesc1$q367*3k3-*s+v=l3t"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config("DEBUG", default=False, cast=bool)


ALLOWED_HOSTS = ["192.168.0.100", "127.0.0.1", "localhost", "https:localhost:8000"]
CSRF_COOKIE_DOMAIN = ".uks1.devtunnels.ms"  # ".github.dev"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pinax.eventlog",
    "shop",
    "accounts",
    "dashboard",
    "cloudinary",
    "crispy_forms",
    "crispy_bootstrap5",
    "colorfield",
    "rest_framework",
]
# assing a custom auth model
AUTH_USER_MODEL = "accounts.User"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]

if not DEBUG:
    # Add WhiteNoise Middleware only when DEBUG is False
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

ROOT_URLCONF = "store.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "shop.utils.context_processors.global_context",
            ],
        },
    },
]


WSGI_APPLICATION = "store.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "store",
    #     "USER": "nasredeen",
    #     "PASSWORD": "Hal@16eem",
    #     "HOST": "localhost",
    #     "PORT": 5432,
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Email Settings

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = "smtp.gmail.com"  # gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "naszattech@gmail.com"
EMAIL_HOST_PASSWORD = "slwn gerb ivty wped"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
if DEBUG:
    # Development settings
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    # Production settings
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# STATIC_URL = "static/"
# MEDIA_URL = "/media/"

# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# # STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATICFILES_DIRS = [
#     (os.path.join(BASE_DIR, "static/")),
#     (os.path.join(BASE_DIR, "media/")),
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Paystack Settings
PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY")


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"#django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST = "smtp.mailgun.org"  # gmail
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "postmaster@sandboxb498bbf25d494b7598ddfb925e9ba85d.mailgun.org"
# EMAIL_HOST_PASSWORD = "2de418cca439c3d5d0bb8159ec88e6b3-5d2b1caa-c70a24a5"

MESSAGE_TAGS = {
    messages.ERROR: "error",
    messages.WARNING: "warning",
    messages.SUCCESS: "success",
    messages.INFO: "info",
}

DOMAIN_NAME = "127.0.0.1:8000"
CRISPY_TEMPLATE_PACK = "bootstrap4"

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)

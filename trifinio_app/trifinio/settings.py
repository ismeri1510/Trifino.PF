"""
Django settings for trifinio project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables desde backend/.env
load_dotenv(BASE_DIR / ".env")


# Seguridad
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-c1_is+52^t1=-#2=zsvxe#$cw5lwm!0!1s8-@n_$(opqu$0*s@",
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]


# Aplicaciones
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # App principal del proyecto
    "core",
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

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

ROOT_URLCONF = "trifinio.urls"


# Templates HTML
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "trifinio.wsgi.application"


# Base de datos Oracle
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": os.getenv("DB_NAME", "localhost:1521/XEPDB1"),
        "USER": os.getenv("DB_USER", "TRIFINIO.PF"),
        "PASSWORD": os.getenv("DB_PASSWORD", "admin"),
    }
}


# Validacion de contrasenas de Django
# Se mantiene aunque el login del proyecto use la tabla usuarios de Oracle.
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


# Internacionalizacion
LANGUAGE_CODE = "es-gt"

TIME_ZONE = "America/Guatemala"

USE_I18N = True

USE_TZ = True


# Archivos static: CSS, JS, imagenes
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# Campo automatico por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

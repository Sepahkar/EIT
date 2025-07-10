from pathlib import Path
import os
from dotenv import load_dotenv

print("\n[~~~~~~~~ Additional Information ~~~~~~~~]\n")

# RUN_IN_PRODUCTION en variable will set in web.config that resides in
# project's root directory
RUN_IN_PRODUCTION = os.getenv("PRODUCTION", False) == "True"

BASE_DIR = Path(__file__).resolve().parent.parent
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # __________APPS____________
    "AccessControl.apps.AccesscontrolConfig",
    "InternalAccess.apps.InternalaccessConfig",
    # __________3RD-PARTY____________
    "django_middleware_global_request",
    "corsheaders",
    "rest_framework",
    "auth2",
    "whitenoise",
]
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.RemoteUserAuthentication",
    ],
}

LANGUAGE_CODE = "fa-ir"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.RemoteUserBackend"]

AUTH_USER_MODEL = "auth2.User"

ROOT_URLCONF = "Config.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "Config.wsgi.application"

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

SESSION_COOKIE_NAME = os.getcwd().split("\\")[-1] + "_sessionid"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


if RUN_IN_PRODUCTION:
    load_dotenv(".env.production")
    ENVIRONMENT_MODE = "PRODUCTION"
    DEBUG = False
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "auth2.middleware.CustomRemoteUserMiddleware",
        "django_middleware_global_request.middleware.GlobalRequestMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    STATIC_ROOT = BASE_DIR / "static"

    print("environment: ", ENVIRONMENT_MODE)


else:
    load_dotenv(".env.dev")
    ENVIRONMENT_MODE = "DEV"
    DEBUG = True
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "auth2.middleware.CustomRemoteUserMiddlewareDEVMODE",
        "django_middleware_global_request.middleware.GlobalRequestMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    DEV_USER = os.getenv("DEV_USER")
    STATICFILES_DIRS = [BASE_DIR / "static"]

    print("environment: ", ENVIRONMENT_MODE)
    print("request.user: ", DEV_USER)

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET = SECRET_KEY
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv("DATABASE_DEFAULT_NAME"),
        "USER": os.getenv("DATABASE_DEFAULT_USER"),
        "PASSWORD": os.getenv("DATABASE_DEFAULT_PASSWORD"),
        "HOST": os.getenv("DATABASE_DEFAULT_HOST"),
        "PORT": os.getenv("DATABASE_DEFAULT_PORT"),
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
        },
    },
}

print("\n[~~~~~~~~ xxxxxxxxxxxxxxxxxxxxxx ~~~~~~~~]\n")
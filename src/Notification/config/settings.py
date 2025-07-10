import os
from pathlib import Path
from dotenv import load_dotenv

print("\n[~~~~~~~~ Additional Information ~~~~~~~~]\n")

# RUN_IN_PRODUCTION en variable will set in web.config that resides in 
# project's root directory
RUN_IN_PRODUCTION = os.getenv("PRODUCTION", False) == "True"

BASE_DIR = Path(__file__).resolve().parent.parent
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'email_service',
    'auth2',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.RemoteUserAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
} 

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "auth2.User"

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.RemoteUserBackend']

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

if RUN_IN_PRODUCTION:
    load_dotenv(".env.production")
    ENVIRONMENT_MODE = "PRODUCTION"
    DEBUG = False
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'auth2.middleware.CustomRemoteUserMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    STATIC_ROOT = BASE_DIR / "static"
 
    # Email configuration
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_HOST_USER =  os.getenv("EMAIL_HOST_USER")
    BCC_EMAIL = os.getenv("BCC_EMAIL")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
    SERVER_EMAIL = os.getenv("SERVER_EMAIL")

    # Admin email for alerts
    ADMIN_EMAILS = os.getenv("ADMINS").split(",")
    ADMINS = [
        (f"admin{i}", email_addr) 
        for i, email_addr
        in enumerate(os.getenv("ADMINS").split(","))
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
        },
        'loggers': {
            'EMAIL_SERVICE': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
        },
    }   

    print("environment: ", ENVIRONMENT_MODE)


else:
    load_dotenv(".env.dev")
    ENVIRONMENT_MODE = "DEV"
    DEBUG = True
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        "auth2.middleware.CustomRemoteUserMiddlewareDEVMODE",
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
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















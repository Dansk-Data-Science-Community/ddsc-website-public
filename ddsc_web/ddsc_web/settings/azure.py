"""
Azure Container Apps production settings.
This settings file is optimized for running the Django application on Azure Container Apps
with Azure Database for PostgreSQL, Azure Cache for Redis, and Azure Blob Storage.
"""
from .settings import *

# Security settings for production
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Azure-specific allowed hosts - will be set via environment variable
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Azure Database for PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB", "ddsc_production"),
        "USER": os.environ.get("POSTGRES_USER", "django"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# Email configuration (Gmail SMTP or Azure Communication Services)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_USE_TLS = True
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# Azure Blob Storage configuration
AWS_STORAGE_BUCKET_NAME = os.environ.get("AZURE_STORAGE_CONTAINER", "ddsc")
AWS_LOCATION = os.environ.get("AZURE_STORAGE_LOCATION", "")  # Empty for root of container

# Azure Blob Storage endpoint (using Azure Storage Account)
AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.environ.get("AZURE_ACCOUNT_KEY")
AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net" if AZURE_ACCOUNT_NAME else None

# Override AWS settings to work with Azure Blob Storage
if AZURE_ACCOUNT_NAME:
    AWS_S3_ENDPOINT_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
    AWS_ACCESS_KEY_ID = AZURE_ACCOUNT_NAME
    AWS_SECRET_ACCESS_KEY = AZURE_ACCOUNT_KEY
    # Static files will be at: https://account.blob.core.windows.net/container/static/
    STATIC_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}/static/"
else:
    # Fallback to DigitalOcean Spaces or S3-compatible storage
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "https://ams3.digitaloceanspaces.com")
    AWS_LOCATION = os.environ.get("AZURE_STORAGE_LOCATION", "prod")
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/"

# TinyMCE JS URL - should point to static files on blob storage
TINYMCE_JS_URL = f"{STATIC_URL}tinymce/tinymce.min.js"

# Event ticket consumption endpoint
CONSUME_TICKET_ENDPOINT = os.environ.get("CONSUME_TICKET_ENDPOINT", "https://ddsc.io/events/consume/")

# Azure Cache for Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
REDIS_SSL = os.environ.get("REDIS_SSL", "true").lower() == "true"

# Construct Redis connection string
if REDIS_PASSWORD:
    REDIS_URL = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0" if REDIS_SSL else f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Celery configuration for Azure
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Django cache with Azure Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# Logging configuration for Azure Container Apps
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

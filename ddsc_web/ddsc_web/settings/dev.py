from .settings import *

DEBUG = True

# only for development
SECRET_KEY = "igv+k0zlu!x6f6l6-8z7nl1p^co6#!3kr_21nqc5+cpdr(2f2h"

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "development",
        "USER": "django",
        "PASSWORD": "L4rxT*vmoBVsFAtzVVQz",
        "HOST": "localhost",
        "PORT": "",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Sometimes it's needed to use smtp backend to check visuals of the email templates
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# local MinIO from docker compose
AWS_STORAGE_BUCKET_NAME = "dev"

AWS_LOCATION = "dev"

AWS_S3_ENDPOINT_URL = "http://localhost:9000"

STATIC_URL = "{}/{}/".format(AWS_S3_ENDPOINT_URL, AWS_LOCATION)

AWS_ACCESS_KEY_ID = "minioadmin"
AWS_SECRET_ACCESS_KEY = "minioadmin"

TINYMCE_JS_URL = os.path.join(STATIC_URL, "static/tinymce/tinymce.min.js")

CONSUME_TICKET_ENDPOINT = "http://localhost:8000/events/consume/"

# Redis settings
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

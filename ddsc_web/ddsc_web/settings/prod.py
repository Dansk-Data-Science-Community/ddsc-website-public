from .settings import *

DEBUG = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "production",
        "USER": "django",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}

ALLOWED_HOSTS = ["ddsc.io", "www.ddsc.io"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")

# DigitalOcean Spaces
AWS_STORAGE_BUCKET_NAME = "ddsc"
AWS_LOCATION = "prod"

STATIC_URL = "{}/{}/".format(AWS_S3_ENDPOINT_URL, AWS_LOCATION)

# TODO: hardcoded url. getting 403 forbidden on other url for some reason.
TINYMCE_JS_URL = (
    "https://ddsc.ams3.digitaloceanspaces.com/static/tinymce/tinymce.min.js"
)

CONSUME_TICKET_ENDPOINT = "https://ddsc.io/events/consume/"

SLACK_INVITATION_LINK = os.environ.get("SLACK_INVITATION_LINK", "https://ddsc.dk/slack")
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
SLACK_WELCOME_CHANNEL = os.environ.get("SLACK_WELCOME_CHANNEL", "#ddsc-welcome")
WELCOME_EMAIL_SENDER = os.environ.get("WELCOME_EMAIL_SENDER", "community@ddsc.dk")

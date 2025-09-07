INSTALLED_APPS += [
    "rest_framework",
    "drf_yasg",
    "ip_tracking",
]

# Celery
CELERY_BROKER_URL = "amqp://localhost"  # RabbitMQ broker
CELERY_RESULT_BACKEND = "rpc://"

# Email (for alerts)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-password"



MIDDLEWARE = [
    # default Django middleware...
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # add IP logging middleware
    "ip_tracking.middleware.IPLoggingMiddleware",
]

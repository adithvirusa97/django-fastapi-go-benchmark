import os
SECRET_KEY = 'benchmark-only'
DEBUG = False
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
INSTALLED_APPS = ['django.contrib.contenttypes', 'benchmark']
MIDDLEWARE = []
DATABASES = {
    'default': {
        "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),

        "CONN_MAX_AGE": 0,
        "CONN_HEALTH_CHECKS": False,
    }
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True

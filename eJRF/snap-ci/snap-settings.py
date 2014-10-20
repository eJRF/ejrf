import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "app_test",
        "USER": "go",
        "PASSWORD": "go",
        "HOST": "localhost",
    }
}

LETTUCE_AVOID_APPS = (
        'south',
        'django_nose',
        'lettuce.django',
        'django_extensions',
        'bootstrap_pagination',
)

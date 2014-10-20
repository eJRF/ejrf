DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "%s" % os.environ['SNAP_DB_PG_NAME'],
        "USER": "%s" % os.environ['SNAP_DB_PG_USER'],
        "PASSWORD": "%s" % os.environ['SNAP_DB_PG_PASSWORD'],,
        "HOST": "%s" % os.environ['SNAP_DB_PG_HOST'],
        "PORT": "%s" % os.environ['SNAP_DB_PG_PORT']
    }
}

LETTUCE_AVOID_APPS = (
        'south',
        'django_nose',
        'lettuce.django',
        'django_extensions',
        'bootstrap_pagination',
)

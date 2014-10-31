from settings import *

DATABASES = {
    'default': {
           "ENGINE": "django.db.backends.postgresql_psycopg2",
           "NAME": "ejrf_test",
           "USER": "ejrf",
           "PASSWORD": "ejrf",
           "HOST": "localhost",
    }
}
SOUTH_TESTS_MIGRATE = False
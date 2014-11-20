"""
Django settings for eJRF project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fwcsq!p9i1m6@%us!hh%8k8o_5ccycphkz0)0wv*^+72)4s-4y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

STATICFILES_DIRS = (
)

STATIC_ROOT = (
    BASE_DIR + "/static"
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'lettuce.django',
    'south',
    'django_extensions',
    'bootstrap_pagination',
    'questionnaire',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bootstrap_pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'eJRF.urls'

WSGI_APPLICATION = 'eJRF.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ejrf",
        "USER": "ejrf",
        "PASSWORD": "ejrf",
        "HOST": "localhost",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LOGIN_REDIRECT_URL = "/"
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = BASE_DIR + "/media/"

UPLOADS_MEDIA_URL = 'user_uploads/'
MEDIA_URL = "media/"

STATIC_URL = '/static/'

ACCEPTED_EXTENSIONS = [".doc", ".docx", ".htm", ".html", ".jpg", ".pdf", ".ppt", ".pptx", ".rtf", ".tif", ".txt",
                       ".xls", ".xlsx"]
MAX_UPLOAD_SIZE = 52428800
# Importing server specific settings
try:
    from localsettings import *
except ImportError, e:
    pass

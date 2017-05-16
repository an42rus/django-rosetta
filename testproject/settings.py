# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import os
import sys
import django

from django.utils.translation import ugettext_lazy as _


SITE_ID = 1

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

PYTHON_VERSION = '%s.%s' % sys.version_info[:2]
DJANGO_VERSION = django.get_version()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'rosetta.db')
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'ROSETTA_TEST'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'translations',
    }
}

TEST_DATABASE_CHARSET = "utf8"
TEST_DATABASE_COLLATION = "utf8_general_ci"

DATABASE_SUPPORTS_TRANSACTIONS = True
SETTINGS_MODULE = 'testproject.settings'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    # 'django.contrib.admin.apps.SimpleAdminConfig',
    # 'django.contrib.redirects.apps.RedirectsConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'rosetta',
]

if django.VERSION[0:2] >= (1, 7):
    INSTALLED_APPS.append('rosetta.tests.test_app.apps.TestAppConfig')

LANGUAGE_CODE = "en"

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

# Note: languages are overridden in the test runner
LANGUAGES = (
    ('bs-Cyrl-BA', u'Bosnian (Cyrillic) (Bosnia and Herzegovina)'),
    ('ja', u'日本語'),
    ('xx', u'XXXXX'),
    ('fr', u'French'),
    ('zh_Hans', u'Chinese (Simplified)'),
    ('fr_FR.utf8', u'French (France), UTF8'),
)

LOCALE_PATHS = [
    os.path.join(PROJECT_PATH, 'locale'),
]

SOUTH_TESTS_MIGRATE = False

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)
STATIC_URL = '/static/'
ROOT_URLCONF = 'testproject.urls'

DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages"
            )
        }
    },
]

STATIC_URL = '/static/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
}

ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'
SECRET_KEY = 'empty'

ROSETTA_ENABLE_REFLANG = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_SHOW_AT_ADMIN_PANEL = True

ROSETTA_ENABLE_ANGULAR_TRANSLATION = True
ROSETTA_ANGULAR_TRANSLATION_FILE_PATH = os.path.join(PROJECT_PATH, 'test_angular_translation_files', 'angular.pot')


"""
Django settings for elearning_academy project
"""

import os
import sys
from ConfigParser import ConfigParser
from datetime import datetime


# Location of main project directory which contains all apps
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")

##TODO
##All these GLOBAL 'constants' should be pushed at one place
COPYRIGHT_YEAR = datetime.today().year
config = ConfigParser()
config.read(os.path.join(PROJECT_DIR, 'elearning_academy/settings.ini'))


DEBUG = config.get('debug', 'debug')
TEMPLATE_DEBUG = config.get('debug', 'template_debug')

ADMINS = (
    ('Alankar Saxena', 'alankar111@gmail.com'),
    ('Aakash Rao', 'aakashns.sky@gmail.com'),
    ('Vinayak Gagrani', 'gagrani.vinayak@gmail.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': config.get('database', 'engine'),
        # Or path to database file if using sqlite3.
        'NAME': config.get('database', 'db_name'),
        # The following settings are not used with sqlite3:
        'USER': config.get('database', 'user'),
        'PASSWORD': config.get('database', 'password'),
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': config.get('database', 'host'),
        # Set to empty string for default.
        'PORT': config.get('database', 'port'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'elearning_academy/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'elearning_academy/staticfiles')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

#Admin Static File URL Prefix
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'elearning_academy/static'),
    os.path.join(PROJECT_DIR, 'discussion_forum/static'),
    os.path.join(PROJECT_DIR, 'concept/static'),
    os.path.join(PROJECT_DIR, 'courseware/static'),
    os.path.join(PROJECT_DIR, 'progress/static'),
    os.path.join(PROJECT_DIR, 'quiz/static'),
    os.path.join(PROJECT_DIR, 'user_profile/static'),
    os.path.join(PROJECT_DIR, 'video/static'),
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('secrets', 'secret_key')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = config.get('server', 'root_urlconf')

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = config.get('server', 'wsgi_location')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'registration/templates'),
    os.path.join(PROJECT_DIR, 'elearning_academy/templates'),
    os.path.join(PROJECT_DIR, 'discussion_forum/templates'),
    os.path.join(PROJECT_DIR, 'courseware/templates'),
    os.path.join(PROJECT_DIR, 'concept/templates'),
    os.path.join(PROJECT_DIR, 'quiz/templates'),
    os.path.join(PROJECT_DIR, 'notification/templates'),
    os.path.join(PROJECT_DIR, 'progress/templates'),
    os.path.join(PROJECT_DIR, 'concept/templates'),
    os.path.join(PROJECT_DIR, 'user_profile/templates'),
    os.path.join(PROJECT_DIR, 'video/templates'),
    os.path.join(PROJECT_DIR, 'courses/templates'),
    os.path.join(PROJECT_DIR, 'assignments/templates'),
    os.path.join(PROJECT_DIR, 'cribs/templates'),
    os.path.join(PROJECT_DIR, 'evaluate/templates'),
    os.path.join(PROJECT_DIR, 'upload/templates'),
    #os.path.join(PROJECT_DIR, 'quiz_template/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    # django 1.2 only
    'django.contrib.messages.context_processors.messages',
    # required by django-admin-tools
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'elearning_academy.context_processor.my_global_name'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',

    #Project Apps
    'util',
    'registration',
    'discussion_forum',

    'user_profile',
    'notification',

    'courseware',
    'quiz',
    'video',
    'concept',
    'document',
    'progress',
    # 'quiz_template',

    #Autograder
    #'easy_thumbnails',
    'guardian',
    'south',
    'djcelery',
    'download',
    'dajax',
    'dajaxice',
    'upload',
    #'profiles',
    'courses',
    'assignments',
    'evaluate',
    'cribs',
    'django.contrib.formtools',

    # Third party apps
    'rest_framework',
    'gunicorn',
)

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

###########################################################################
##TODO Alot of hard coding in the following sections, should be chucked off
###########################################################################
# Setting for Django Rest Framework
REST_FRAMEWORK = {
    # Pagination Offset
    'PAGINATE_BY': 10,
    # Allow client to override, using `?page_size=xxx`.
    'PAGINATE_BY_PARAM': 'page_size',
    # Maximum limit allowed when using `?page_size=xxx`.
    #'MAX_PAGINATE_BY': 100,

    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': (
        'rest_framework.serializers.HyperlinkedModelSerializer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    # Allowing only Authenticated users to read API
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    # Limiting access of User by throttling requests
    'DEFAULT_THROTTLE_CLASSES': (
        #'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '200/min'
    }
}

LOGIN_REDIRECT_URL = '/courseware/'

AUTH_PROFILE_MODULE = 'user_profile.CustomUser'
ANONYMOUS_USER_ID = -1

EMAIL_HOST = config.get('email', 'host')
EMAIL_PORT = config.get('email', 'port')

EMAIL_HOST_USER = config.get('email', 'user')
EMAIL_HOST_PASSWORD = config.get('email', 'password')
EMAIL_USE_TLS = config.get('email', 'use_TLS')
EMAIL_BACKEND = config.get('email', 'backend')

##TODO
##Hack to implement http for now, this should go to
##settings.ini
MY_SERVER = "http://" + config.get('server', 'ip')
MY_SITE_NAME = config.get('server', 'name')

DEFAULT_CONCEPT_IMAGE = config.get('server', 'default_concept_image')
TITLE_ICON = config.get('server', 'title_icon')


#for changing database of testing
# If manage.py test was called, use SQLite for faster testing
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test_sqlite.db'
        }
    }

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
    )
else:
    #added by Vinayak
    #Fixtures to load data automatically when migrate is called
    #gives error while runnint tests
    FIXTURE_DIRS = (
        os.path.join(PROJECT_DIR, 'elearning_academy/fixtures'),
        os.path.join(PROJECT_DIR, 'user_profile/fixtures'),
        os.path.join(PROJECT_DIR, 'courseware/fixtures'),
    )

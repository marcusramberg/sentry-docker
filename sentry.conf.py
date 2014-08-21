# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *  # noqa
import os.path

from decouple import config
import dj_database_url
import django_cache_url

CONF_ROOT = os.path.dirname(__file__)
DATA_DIR = '/data'
DEFAULT_SQLITE_DB_PATH = os.path.join(DATA_DIR, 'sentry.db')

REDIS_HOST = config('SENTRY_REDIS_HOST', default='redis')
REDIS_PORT = config('SENTRY_REDIS_PORT', default=6379, cast=int)

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///{0}'.format(DEFAULT_SQLITE_DB_PATH))
}

if 'postgres' in DATABASES['default']['ENGINE']:
    DATABASES['default']['OPTIONS'] = {
        'autocommit': True,
    }

CACHES = {'default': django_cache_url.config(default='hiredis://{0}:{1}/2/'.format(REDIS_HOST, REDIS_PORT))}

###########
# Queue ##
###########

# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

# You can enable queueing of jobs by turning off the always eager setting:
CELERY_ALWAYS_EAGER = config('CELERY_ALWAYS_EAGER', default=True, cast=bool)
DEFAULT_BROKER_URL = 'redis://{0}:{1}/1'.format(REDIS_HOST, REDIS_PORT)

BROKER_URL = config('SENTRY_BROKER_URL', default=DEFAULT_BROKER_URL)

####################
# Update Buffers ##
####################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

# You'll need to install the required dependencies for Redis buffers:
#   pip install redis hiredis nydus
#
SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
SENTRY_REDIS_OPTIONS = {
    'hosts': {
        0: {
            'host': REDIS_HOST,
            'port': REDIS_PORT,
        }
    }
}

################
# Web Server ##
################

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = config('SENTRY_URL_PREFIX')  # No trailing slash!

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# and X-Forwarded-Host headers, and uncomment the following settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True

SENTRY_WEB_HOST = config('SENTRY_WEB_HOST', default='0.0.0.0')
SENTRY_WEB_PORT = config('SENTRY_WEB_PORT', default=9000, cast=int)
SENTRY_WEB_OPTIONS = {
    'workers': config('SENTRY_WORKERS', default=3, cast=int),  # the number of gunicorn workers
    'limit_request_line': 0,  # required for raven-js
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'errorlog' : os.path.join(DATA_DIR, 'gunicorn_error.log'),
    'accesslog' : os.path.join(DATA_DIR, 'gunicorn_access.log'),
}

#################
# Mail Server ##
#################

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = config('SENTRY_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

EMAIL_HOST = config('SENTRY_EMAIL_HOST', default='localhost')
EMAIL_HOST_PASSWORD = config('SENTRY_EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('SENTRY_EMAIL_HOST_USER', default='')
EMAIL_PORT = config('SENTRY_EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('SENTRY_EMAIL_USE_TLS', default=False, cast=bool)

# The email address to send on behalf of
SERVER_EMAIL = config('SENTRY_SERVER_EMAIL', default='root@localhost')

###########
# etc. ##
###########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = config('SECRET_KEY')

# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless. We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_KEY', default='')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET', default='')

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = config('FACEBOOK_APP_ID', default='')
FACEBOOK_API_SECRET = config('FACEBOOK_API_SECRET', default='')

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = config('GOOGLE_OAUTH2_CLIENT_ID', default='')
GOOGLE_OAUTH2_CLIENT_SECRET = config('GOOGLE_OAUTH2_CLIENT_SECRET', default='')

# https://github.com/settings/applications/new
GITHUB_APP_ID = config('GITHUB_APP_ID', default='')
GITHUB_API_SECRET = config('GITHUB_API_SECRET', default='')

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = config('TRELLO_API_KEY', default='')
TRELLO_API_SECRET = config('TRELLO_API_SECRET', default='')

# https://confluence.atlassian.com/display/BITBUCKET/OAuth+Consumers
BITBUCKET_CONSUMER_KEY = config('BITBUCKET_CONSUMER_KEY', default='')
BITBUCKET_CONSUMER_SECRET = config('BITBUCKET_CONSUMER_SECRET', default='')

# custom settings
ALLOWED_HOSTS = ['*']
LOGGING['disable_existing_loggers'] = False
# Django settings for rapidsmsrw1000 project.

import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rapidsmsrw1000_db',
        'USER': 'root',
        'PASSWORD': '123',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Kigali'

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
    
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hei&amp;p)mzo_k(ydn&amp;1mt0i%d8f%li22wk^ka_d^(1h2o3@lg(n9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rapidsmsrw1000.urls'
BASE_TEMPLATE = 'layout.html'
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rapidsmsrw1000.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
    
    
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

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
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'basic',
            'filename': os.path.join(PROJECT_PATH, 'rapidsms.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'blockingrouter': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # External apps
    "django_nose",
    "djtables",
    "rapidsms",
    "rapidsms.contrib.handlers",
    "rapidsms.contrib.default",
    "rapidsms.contrib.export",
    "rapidsms.contrib.httptester",
    #"rapidsms.contrib.locations",
    "rapidsms.contrib.messagelog",
    "rapidsms.contrib.messaging",
    "rapidsms.contrib.registration",
    "rapidsms.contrib.scheduler",
    "rapidsms.contrib.echo",

	#DEVELOPED APPS
	
	"rapidsmsrw1000.apps.ubuzima",
	"rapidsmsrw1000.apps.locations",
	"rapidsmsrw1000.apps.reporters",
	"rapidsmsrw1000.apps.patterns",
	"rapidsmsrw1000.apps.parsers",
	"rapidsmsrw1000.apps.chws",
	"rapidsmsrw1000.apps.ambulances",
	"rapidsmsrw1000.apps.webapp",
	"rapidsmsrw1000.apps.thousanddays",
	
)

INSTALLED_BACKENDS = {
    "message_tester": {
        "ENGINE": "rapidsms.contrib.httptester.backend",
    },
	# other backends, if any
    "kannel-fake-smsc" : {
        "ENGINE":  "rapidsms.backends.kannel.outgoing",
        "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
        "sendsms_params": {"smsc": "FAKE",
                           "from": "123", # not set automatically by SMSC
                           "username": "rapidsms",
                           "password": "CHANGE-ME"}, # or set in localsettings.py
        "coding": 0,
        "charset": "ascii",
        "encode_errors": "ignore", # strip out unknown (unicode) characters
    },

	# ...
    "kannel-usb0-smsc" : {
        "ENGINE":  "rapidsms.backends.kannel.outgoing",
        "sendsms_url": "http://127.0.0.1:13013/cgi-bin/sendsms",
        "sendsms_params": {"smsc": "usb0-modem",
                           "from": "+SIMphonenumber", # not set automatically by SMSC
                           "username": "rapidsms",
                           "password": "CHANGE-ME"}, # or set in localsettings.py
        "coding": 0,
        "charset": "ascii",
        "encode_errors": "ignore", # strip out unknown (unicode) characters
    },
}

# this rapidsms-specific setting defines which views are linked by the
# tabbed navigation. when adding an app to INSTALLED_APPS, you may wish
# to add it here, also, to expose it in the rapidsms ui.
RAPIDSMS_TABS = [
    ("rapidsms.contrib.messagelog.views.message_log",       "Message Log"),
    ("rapidsms.contrib.registration.views.registration",    "Registration"),
    ("rapidsms.contrib.messaging.views.messaging",          "Messaging"),
    #("rapidsms.contrib.locations.views.locations",          "Map"),
    ("rapidsms.contrib.scheduler.views.index",              "Event Scheduler"),
    ("rapidsms.contrib.httptester.views.generate_identity", "Message Tester"),
]

LOGIN_REDIRECT_URL = '/'

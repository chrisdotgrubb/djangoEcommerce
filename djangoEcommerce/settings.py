import os.path
from pathlib import Path
from django.contrib.messages import constants as message_constants
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=pg0-lf1ut4d7dwt%o7hgeaf5#9g1te3!4+-yc1^tvq5ko)@h8'

DEBUG = True

ALLOWED_HOSTS = ['localhost']

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'store',
	'user',
	'cart',
	'payment',
	'order',
	'django_htmx',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django_htmx.middleware.HtmxMiddleware'
]

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
			'formatter': 'format_1',
		},
	},
	'formatters': {
		'format_1': {
			'format': '({levelname}) [{pathname}:{funcName}:{lineno:d}] "{message}" ({levelname})',
			'style': '{',
		},
	},
	'root': {
		'handlers': ['console'],
		'level': 'DEBUG',
	},
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MESSAGE_LEVEL = message_constants.DEBUG

ROOT_URLCONF = 'djangoEcommerce.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'store.context_processors.categories',
				'cart.context_processors.cart'
			],
		},
	},
]

WSGI_APPLICATION = 'djangoEcommerce.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

AUTH_USER_MODEL = 'user.MyUser'
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/user/dashboard/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True

COUNTRIES_OVERRIDE = {'US': _('United States')}
COUNTRIES_FIRST = ['US']
COUNTRIES_FIRST_BREAK = '-----------'
COUNTRIES_FIRST_REPEAT = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static/']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'US'

from .base import *

DEBUG = False
ALLOWED_HOSTS = ['54.202.38.92']

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.postgresql",
		"NAME": os.getenv('DB_NAME'),
		"USER": os.getenv('DB_USER'),
		"PASSWORD": os.getenv('DB_PASSWORD'),
		"HOST": os.getenv('DB_HOST'),
		"PORT": os.getenv('DB_PORT'),
	}
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'newsletter@rental-insight.com'
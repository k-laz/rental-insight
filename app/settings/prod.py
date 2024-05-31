from .base import *

DEBUG = False
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT = True


# HTTP Strict Transport Security (HSTS) is a security feature that tells browsers to only communicate with your site over HTTPS. 
# This helps prevent man-in-the-middle attacks.
# This specifies the duration (in seconds) that the browser should remember to only use HTTPS. 
# A common setting is 31536000 seconds (1 year).
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True




ALLOWED_HOSTS = ['dev-env-1.us-west-2.elasticbeanstalk.com']


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
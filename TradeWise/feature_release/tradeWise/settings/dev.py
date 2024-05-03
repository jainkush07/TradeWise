from .base import *

SECRET_KEY = '8#@#hrea=v2o5=)jq4_n$uxqki7!rpllslx+zr_0j@88#ki3#w'

DEBUG = True

ALLOWED_HOSTS = ['dev.planify.in','*',]

ADMINS = (
	('Inwoin Technologies', 'client-dev-reports@inwoin.com'),
)


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AWS_S3_OBJECT_PARAMETERS = {
	'CacheControl': 'max-age=86400',
}

SIMPLE_JWT = {
	'SIGNING_KEY': SECRET_KEY,
	'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
	'VERIFYING_KEY': SECRET_KEY,
}

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

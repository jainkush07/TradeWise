from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'rest_framework',
    'social_django',
    'excelUtilityApp',
    'authNewApp',
    'utilityApp',
    'authApp',
    'investorApp',
    'dmFormsApp',
    'brokenRedirectApp',
    'staticPagesSlugApp',
    'stockPriceApp',
    'whatsappAuthApp',
    'websiteApp',
    'stockApp',
    'blogHomeApp',
    'videoBlogApp',
    'articleBlogApp',
    'employeeApp',
    'mediaBlogApp',
    'newsBlogApp',
    'videoShortsApp',
    'productPagesApp',
    'screenerStoreApp',
    'cartApp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'crispy_forms',
    'django_summernote',
    'import_export',
    'sorl.thumbnail',
    'django_ses',
    'storages',
    'taggit',
    'taggit_autosuggest',
    'mptt',
    'django_filters',
    'rest_framework_simplejwt'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'authApp.middleware.AuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

ROOT_URLCONF = 'planifyMain.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'stockTags': 'stockApp.templatetags.stockTags'
            }
        },
    },
]

WSGI_APPLICATION = 'planifyMain.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

X_FRAME_OPTIONS = 'SAMEORIGIN'
THUMBNAIL_FORCE_OVERWRITE = True
THUMBNAIL_DEBUG = True
CRISPY_TEMPLATE_PACK = 'bootstrap4'
SUMMERNOTE_THEME = 'lite'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

AWS_LOCATION = 'static'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'planifyMain.storage_backends.MediaStorage'

IMPORT_EXPORT_USE_TRANSACTIONS = True

handler404 = 'stockApp.views.handler404'
handler500 = 'stockApp.views.handler500'

TAGGIT_CASE_INSENSITIVE = True

SETTINGS_EXPORT = [
    'MEDIA_LOCATION',
    'AWS_STORAGE_BUCKET_NAME',
]

LOGIN_URL = 'authNewApp:login_signup_first_url'
LOGOUT_URL = 'authNewApp:logout_url'
UPDATE_WHATSAPP_TO_ACCOUNT_URL = 'authNewApp:user_whatsapp_update_url'
UPDATE_EMAIL_TO_ACCOUNT_URL = 'authNewApp:user_email_update_url'
CHANGE_PASSWORD_URL = 'authNewApp:create_or_update_user_password_url'
LOGIN_REDIRECT_URL = 'websiteApp:startupPageUrl'
LOGIN_PIN_URL = 'authNewApp:try_login_by_pin_url'

# session
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_LOGIN_ERROR_URL = 'authNewApp:login_signup_first_url'
SOCIAL_AUTH_LOGIN_URL = 'authNewApp:login_signup_first_url'
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_emailaddress', ]
SOCIAL_AUTH_LOGIN_LINKEDIN_URL = "authApp:social_login_url"
SOCIAL_AUTH_LOGIN_GOOGLE_URL = "authApp:social_login_url"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "authApp:social_login_url"
SOCIAL_AUTH_LOGIN_URL = "authApp:social_login_url"
SOCIAL_AUTH_LOGIN_ERROR_URL = 'authApp:social_login_url'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# PG
CART_SESSION_ID = 'cart'
BASE_URL = 'https://testing.tradewise.in'
LINKED_IN_APP_AUTH_KEY = ''
LINKED_IN_APP_AUTH_SECRET = ''
FCM_SECRET_KEY = 'key=AAAA2xoO-_s:APA91bEe6mIZJHv9dfrCfdZSV2NogUbS-HHqZ8smWaZvYBwN7gIEtpMoHcB1j-Cbg5Jw_eMllXO90HZEyvphkmQJldTovvNAD0BCjCPRJ_-nL2plMLDXJrTVEV3K7GKdPyfdgWecNSi7'

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'django-insecure-mzb*)qg!t7w2$-*20+pqsvr&i54)jl*=i_3+e0^uh7du(vdro0'
HOST = os.environ.get('HOST')

# DEBUG = 'localhost' in HOST
DEBUG = 'localhost' in HOST or 'docker-sandbox' in HOST
CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = [
    '*',
]

#CORS settings
CORS_ALLOWED_ORIGINS = [
    'https://localhost',
    'https://localhost:3000',
    'http://localhost',
    f"https://{HOST}",
    f"http://{HOST}",
]

CSRF_TRUSTED_ORIGINS = [
    *CORS_ALLOWED_ORIGINS,
]

USE_X_FORWARDED_HOST = True

# Application definition
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'solo',
    'adminsortable2',
    'streamfield',
    'tinymce',
    'mptt',
    'django_apscheduler',

    'apps.config',
    'apps.diaries',
    'apps.local_hierarchy',
    'apps.notification',
    'apps.task_manager',
    'apps.library',
    'apps.users',
    'apps.wishlist',
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 15

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

STREAMFIELD_SHOW_ADMIN_COLLAPSE = True

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'system.middleware.HostOverrideMiddleware',
    'system.middleware.SwitchNameingStyleMiddleware',
]

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "system/templates/"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'system.wsgi.application'

# TINYMCE WYSIWYG editor config

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 600,
    "width": 1000,
    'relative_urls': False,
    'content_css': '/admin/style/main.css',
    'document_base_url': '/media/',
    "plugins": "advlist autolink lists link image charmap preview anchor table \
                searchreplace visualblocks code fullscreen insertdatetime media table \
                help wordcount",
    "toolbar": "styleselect | formatselect fontselect | code | table | \
                bold italic backcolor | alignleft aligncenter \
                alignright alignjustify | bullist numlist outdent indent | \
                removeformat",
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {     
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PG_DATABASE'),
        'USER': os.environ.get('PG_USERNAME'),
        'PASSWORD': os.environ.get('PG_PASSWORD'),
        'HOST': os.environ.get('PG_HOST'),
        'PORT': 5432,
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_ROOT_WEBP = BASE_DIR
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main': {
            'format': '[{asctime}] [{levelname}] |{pathname}:{lineno}|: {message}',
            'style': '{',
        },
        'short': {
            'format': '[{asctime}] [{levelname}]: {message}',
            'style': '{',
        },
    },
    'handlers':{
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main',
        },
        'main_file': {
            'class': 'logging.FileHandler',
            'formatter': 'main',
            'filename': 'logs/main.log',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console', 'main_file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# Email settings
EMAIL_HOST = 'mail.system.place-start.ru'
EMAIL_PORT = 250
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')

DEFAULT_FROM_EMAIL = f"{HOST.split('.')[0]}@docker.ps"
import os
from datetime import timedelta
from celery.schedules import crontab
import environ

# region ---------------------- BASE CONFIGURATION -----------------------------------------
root = environ.Path(__file__) - 2  # Define the project root directory
env = environ.Env()  # Initialize environment variables handler
environ.Env.read_env(env.str(root(), '.env'))  # Load the .env file
BASE_DIR = root()

# Security and Debug Configuration
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

# Allowed Hosts (space-separated string converted to a list)
ALLOWED_HOSTS = env.str('ALLOWED_HOSTS', default='').split(' ')
# endregion ---------------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-part applications
    'corsheaders',
    'drf_spectacular',
    'rest_framework',
    'django_filters',
    'djoser',
    'phonenumber_field',

    # Applications for my project
    'api',
    'common',
    'users',
    'clients',
    'analytics',

]

# region ---------------------- CORS HEADERS -----------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True  # Allow all origins
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']  # Allow all headers
CSRF_COOKIE_SECURE = False  # Disable CSRF cookie for development
# endregion ---------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# region ------------------------- DATABASE CONFIGURATION -----------------------------------
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': env.str('PG_DATABASE', default='postgres'),
    #     'USER': env.str('PG_USER', default='postgres'),
    #     'PASSWORD': env.str('PG_PASSWORD', default='postgres'),
    #     'HOST': env.str('DB_HOST', default='localhost'),
    #     'PORT': env.int('DB_PORT', default=5433),
    # },
    'default': {  # Optional SQLite database for testing
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# endregion ---------------------------------------------------------------------------------

# region ---------------------- REST FRAMEWORK ----------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# endregion -------------------------------------------------------------------------

# region ---------------------- SIMPLE JWT & DJOSER -----------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SERIALIZERS': {
        'user_create': 'users.serializers.api.serializer_user.RegistrationSerializer',
        'user': 'users.serializers.api.serializer_user.UserListSerializer',
        'current_user': 'users.serializers.api.serializer_user.UserListSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
}
# endregion -------------------------------------------------------------------------

# region ---------------------- SPECTACULAR SETTINGS --------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': '',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'SERVE_AUTHENTICATION': [
        'rest_framework.authentication.BasicAuthentication',
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        "displayOperationId": True,
        "syntaxHighlight.active": True,
        "syntaxHighlight.theme": "arta",
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": True,
    },

    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,

    'ENABLE_DJANGO_DEPLOY_CHECK': False,
    'DISABLE_ERRORS_AND_WARNINGS': True,
}
# endregion -------------------------------------------------------------------


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


# region ---------------------- LOCALIZATION ------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True  # Enable internationalization
USE_TZ = True    # Enable timezone support
# endregion ---------------------------------------------------------------------------------


# region ---------------------- CELERY ------------------------------------------------

# Использование брокера сообщений для Celery (Redis)
CELERY_BROKER_URL = os.getenv("REDDIS_URL", "redis://localhost:6379/0")

# Использование Redis для хранения результатов выполнения задач
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Отслеживание состояния выполнения задач (по умолчанию выключено)
CELERY_TASK_TRACK_STARTED = os.getenv("CELERY_TASK_TRACK_STARTED", "False").lower() in ("true", "1", "yes")

# Максимальное время выполнения задачи (30 минут)
CELERY_TASK_TIME_LIMIT = 30 * 60

# Поддерживаемые форматы сериализации данных
CELERY_ACCEPT_CONTENT = [os.getenv("ACCEPT_CONTENT", "json")]
CELERY_RESULT_SERIALIZER = os.getenv("RESULT_SERIALIZER", "json")
CELERY_TASK_SERIALIZER = os.getenv("TASK_SERIALIZER", "json")

# Указание временной зоны сервера для корректного выполнения задач по расписанию
CELERY_TIMEZONE = os.getenv("TIMEZONE",)

# Настройка периодических задач Celery Beat
CELERY_BEAT_SCHEDULE = {
    "backup_database": {
        # Путь к задаче, указанной в model_tk.py
        "task": "common.tasks.db_backup_task",
        # Резервное копирование БД каждый день в полночь
        "schedule": crontab(hour=0, minute=0),
    },
}

# endregion ---------------------------------------------------------------------------------

# region ------------------------- STATIC AND MEDIA ----------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_TEST_ROOT = os.path.join(BASE_DIR, 'media/test/')
# endregion ---------------------------------------------------------------------------------


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# region ---------------------- SMTP ------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Настройка почтового сервера по SMTP-протоколу
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# endregion ---------------------------------------------------------------------------------
import os
from pathlib import Path

from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv(".env")

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = bool(os.environ.get("DJANGO_DEBUG"))
ALLOWED_HOSTS = []

# Django приложения по умолчанию
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Сторонние расширения (пока не используются)
THIRD_PARTY_APPS = [
    # Здесь будут добавляться сторонние пакеты, например:
    # "rest_framework",
    # "django_filters",
    # "crispy_forms",
]

# Локальные приложения проекта
LOCAL_APPS = [
    "users.apps.UsersConfig",
    "products.apps.ProductsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Django middleware по умолчанию
DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Сторонние middleware (пока не используются)
THIRD_PARTY_MIDDLEWARE = [
    # Здесь будут добавляться сторонние middleware, например:
    # "django.middleware.locale.LocaleMiddleware",
]

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

ROOT_URLCONF = "MediaMarket.urls"

# Django контекст-процессоры по умолчанию
DJANGO_CONTEXT_PROCESSORS = [
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]

# Локальные контекст-процессоры проекта
LOCAL_CONTEXT_PROCESSORS = [
    "products.context_processors.year.year",
    "products.context_processors.cart.count_cart",
    "products.context_processors.favorite.favorite_count",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": DJANGO_CONTEXT_PROCESSORS + LOCAL_CONTEXT_PROCESSORS
        },
    }
]

WSGI_APPLICATION = "MediaMarket.wsgi.application"


# Настройки базы данных

# SQLite3
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

# PostgreSQL
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRE_NAME"),
#         "USER": os.environ.get("POSTGRE_USER"),
#         "PASSWORD": os.environ.get("POSTGRE_PASSWORD"),
#         "HOST": os.environ.get("POSTGRE_HOST"),
#         "PORT": os.environ.get("POSTGRE_PORT"),
#     }
# }


# Стандартные валидаторы паролей Django
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
        "MESSAGE": "Ваш пароль не может быть слишком похож на вашу другую личную информацию.",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "MESSAGE": "Ваш пароль должен содержать не менее 8 символов.",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        "MESSAGE": "Ваш пароль не может быть широко используемым паролем.",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        "MESSAGE": "Ваш пароль не может состоять только из цифр.",
    },
]

# Международизация и локализация
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# Статические файлы и медиа
STATIC_URL = "static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Настройки Django
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Кастомная модель пользователя
AUTH_USER_MODEL = "users.CustomUser"

# URL для аутентификации
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "products:products_list"
LOGOUT_REDIRECT_URL = "users:login"

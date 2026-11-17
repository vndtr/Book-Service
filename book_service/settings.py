"""Настройки Django-проекта Book Service."""

from pathlib import Path

# Корень репозитория: каталог, в котором лежит manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# Ключ учебного проекта; в рабочей версии его выносят из кода
SECRET_KEY = (
    "django-insecure-"
    "k7#bs2v@x9q!m4r%t1w&z8c^n5y(d3f)h6j+l0p_a-e=u"
)
# Режим отладки. Для проверки собственной страницы 404 временно
# устанавливается False (см. раздел 5.4.7), после проверки возвращается True.
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage",
    "books",
    "users",
    # Инструмент анализа запросов и отладки.
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "book_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Общие данные Book Service для всех шаблонов.
                "books.context_processors.book_context",
            ],
        },
    },
]

WSGI_APPLICATION = "book_service.wsgi.application"

# Целевая база Django (db.sqlite3): модели User и Book работают через ORM.
# Исходная база ПР7 (data/library.sqlite) нужна только для переноса данных.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Загруженные пользователями файлы (обложки книг).
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

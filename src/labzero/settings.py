import os
from pathlib import Path

import environ

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    _ = lambda s: s  # noqa: E731


def get_base_settings(BASE_DIR=None):
    """
    Returns base settings dictionary for labzero projects.
    """
    if BASE_DIR is None:
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
    else:
        BASE_DIR = Path(BASE_DIR)

    env = environ.Env()
    print(BASE_DIR)
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        environ.Env.read_env(env_file=str(env_file))

    # Quick-start development settings - unsuitable for production
    SECRET_KEY = env.str(
        "SECRET_KEY",
        default="PRe0vrb9nRb1qMftrg1gEuETn6ui9FbyeRVx6Y1716lN30Dg0qL8BhdOkzW",
    )

    DEBUG = env.bool("DEBUG", default=False)
    ALLOWED_HOSTS = ["*"]

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "djangomix",
        "django_umin",
        "labzero",
        "wagtail.contrib.forms",
        "wagtail.contrib.redirects",
        "wagtail.embeds",
        "wagtail.sites",
        "wagtail.users",
        "wagtail.snippets",
        "wagtail.documents",
        "wagtail.images",
        "wagtail.search",
        "wagtail.admin",
        "wagtail",
        "modelcluster",
        "taggit",
    ]

    if DEBUG:
        INSTALLED_APPS.append("django_extensions")

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    ]

    CSRF_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SECURE = True

    LANGUAGES = [
        ("en", _("English")),
    ]

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.media",
                ],
            },
        },
    ]

    # Database
    DATABASES = {"default": env.db()}
    DATABASES["default"]["TEST"] = {
        "NAME": "labzero_test",
        "USER": "labzero_test",
    }

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    AUTH_USER_MODEL = "labzero.User"

    # Internationalization
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files
    STATIC_URL = "/static/"
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
    STATIC_ROOT = os.path.join(BASE_DIR, "public")

    # DJANGOMIX
    PUBLIC_URL = LARAVELMIX_PUBLIC_URL = STATIC_URL + "mix/build"
    MANIFEST_DIRECTORY = LARAVELMIX_MANIFEST_DIRECTORY = os.path.join(
        BASE_DIR, "static/mix/build"
    )

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    SIMPLE_CUSTOMIZE_MODE = env.str("SIMPLE_CUSTOMIZE_MODE", True)

    LOGIN_URL = "/login/"
    LOGIN_REDIRECT_URL = "/app/"
    LOGOUT_REDIRECT_URL = "/"

    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

    WAGTAIL_SITE_NAME = "LabZero App"

    return {
        "BASE_DIR": BASE_DIR,
        "SECRET_KEY": SECRET_KEY,
        "DEBUG": DEBUG,
        "ALLOWED_HOSTS": ALLOWED_HOSTS,
        "INSTALLED_APPS": INSTALLED_APPS,
        "MIDDLEWARE": MIDDLEWARE,
        "CSRF_COOKIE_SAMESITE": CSRF_COOKIE_SAMESITE,
        "CSRF_COOKIE_SECURE": CSRF_COOKIE_SECURE,
        "LANGUAGES": LANGUAGES,
        "TEMPLATES": TEMPLATES,
        "DATABASES": DATABASES,
        "AUTH_PASSWORD_VALIDATORS": AUTH_PASSWORD_VALIDATORS,
        "AUTH_USER_MODEL": AUTH_USER_MODEL,
        "LANGUAGE_CODE": LANGUAGE_CODE,
        "TIME_ZONE": TIME_ZONE,
        "USE_I18N": USE_I18N,
        "USE_L10N": USE_L10N,
        "USE_TZ": USE_TZ,
        "STATIC_URL": STATIC_URL,
        "STATICFILES_DIRS": STATICFILES_DIRS,
        "STATIC_ROOT": STATIC_ROOT,
        "PUBLIC_URL": PUBLIC_URL,
        "LARAVELMIX_PUBLIC_URL": LARAVELMIX_PUBLIC_URL,
        "MANIFEST_DIRECTORY": MANIFEST_DIRECTORY,
        "LARAVELMIX_MANIFEST_DIRECTORY": LARAVELMIX_MANIFEST_DIRECTORY,
        "MEDIA_URL": MEDIA_URL,
        "MEDIA_ROOT": MEDIA_ROOT,
        "SIMPLE_CUSTOMIZE_MODE": SIMPLE_CUSTOMIZE_MODE,
        "LOGIN_URL": LOGIN_URL,
        "LOGIN_REDIRECT_URL": LOGIN_REDIRECT_URL,
        "LOGOUT_REDIRECT_URL": LOGOUT_REDIRECT_URL,
        "CSRF_TRUSTED_ORIGINS": CSRF_TRUSTED_ORIGINS,
        "WAGTAIL_SITE_NAME": WAGTAIL_SITE_NAME,
    }

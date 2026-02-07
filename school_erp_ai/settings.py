
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6rq8cev3bk$!fvaa3k-hy8(5!m*z(&gkfx+++k#!8%-vh42y1="

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get("DEBUG", "False") == "True"

#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
DEBUG = True
ALLOWED_HOSTS = []

#DEBUG = False
#ALLOWED_HOSTS = ["school-erp-l2en.onrender.com"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts.apps.AccountsConfig",
    "admission.apps.AdmissionConfig",

    "schools",
    "classrooms",
    "students",
    "teacher",
    "attendance",
    "leads",
    "fees",
    "exams",
    "parents",
    "notices",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "schools.middleware.SchoolContextMiddleware",
    
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "school_erp_ai.middleware.RoleRedirectMiddleware",
]

ROOT_URLCONF = "school_erp_ai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [ BASE_DIR / 'templates' ],  # 🔥 IMPORTANT
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
WSGI_APPLICATION = "school_erp_ai.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "erp@school.com"
ADMIN_EMAIL = "admin@school.com"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = 'accounts.User'

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/schools/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/post-login/"
LOGOUT_REDIRECT_URL = "/login/"

if os.environ.get("DJANGO_SUPERUSER_USERNAME"):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(
            username=os.environ["DJANGO_SUPERUSER_USERNAME"]
        ).exists():
            User.objects.create_superuser(
                os.environ["DJANGO_SUPERUSER_USERNAME"],
                os.environ["DJANGO_SUPERUSER_EMAIL"],
                os.environ["DJANGO_SUPERUSER_PASSWORD"],
            )
    except Exception:
        pass

JAZZMIN_SETTINGS = {
    # Branding
    "site_title": "School ERP",
    "site_header": "School ERP Dashboard",
    "site_brand": "School ERP",
    "site_logo": "images/logo.png",
    "login_logo": None,
    "login_logo_dark": None,
    "welcome_sign": "Welcome to School ERP",
    "copyright": "School ERP © 2026",

    # UI
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": False,

    # Search
    "search_model": [
        "accounts.User",
        "students.Student",
    ],

    # Top menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "View Site", "url": "/", "new_window": True},
    ],

    # Sidebar icons
    "icons": {
        # Apps
        "auth": "fas fa-users-cog",
        "accounts": "fas fa-user-shield",
        "students": "fas fa-user-graduate",
        "attendance": "fas fa-calendar-check",
        "fees": "fas fa-rupee-sign",
        "parents": "fas fa-users",
        "exams": "fas fa-file-alt",
        "schools": "fas fa-school",
        "teacher": "fas fa-chalkboard-teacher",
        "leads": "fas fa-phone",

        # Models
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user",
        "students.Student": "fas fa-user-graduate",
        "attendance.Attendance": "fas fa-calendar-day",

        "fees.FeePayment": "fas fa-cash-register",
        "fees.FeeStructure": "fas fa-money-check-alt",

        "parents.Parent": "fas fa-user-friends",

        "exams.Exam": "fas fa-file-alt",
        "exams.Subject": "fas fa-book",
        "exams.Result": "fas fa-poll",

        "schools.School": "fas fa-school",
        "teacher.Teacher": "fas fa-chalkboard-teacher",
        "leads.Lead": "fas fa-phone-volume",
    },

    # Sidebar order (VERY IMPORTANT)
    "order_with_respect_to": [
        "accounts",
        "students",
        "attendance",
        "fees",
        "parents",
        "exams",
        "schools",
        "teacher",
        "leads",
        "auth",
    ],

    # Default icons
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
}

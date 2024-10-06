from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-7gnr974ckmmmh0l(l&ru^x3@ig)nxxbz85#1%kvrkxq=2baa19'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "paper_admin",
    "paper_admin.patches.django_money",  
    "paper_admin.patches.django_solo",   
    "paper_admin.patches.mptt",          
    "paper_admin.patches.logentry_admin",
    "paper_admin.patches.tree_queries",  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'home',
    'dashboard',
    'django.contrib.humanize',
    'django_ckeditor_5',
    'cities_light',
    'crispy_forms',
    'crispy_tailwind',
    # 'compressor',
]

AUTH_USER_MODEL = 'dashboard.CustomUser'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zainly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'home.context_processors.custom_site_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zainly.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT=os.path.join(BASE_DIR,'staticfiles/media/')
MEDIA_URL="/media/"

# STATICFILES_DIRS =[
#     os.path.join(BASE_DIR, "static"),
# ]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = '/social-auth/login/google-oauth2/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False


CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['IN']  # Limit to India

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
customColorPalette = [
      {
          'color': 'hsl(4, 90%, 58%)',
          'label': 'Red'
      },
      {
          'color': 'hsl(340, 82%, 52%)',
          'label': 'Pink'
      },
      {
          'color': 'hsl(291, 64%, 42%)',
          'label': 'Purple'
      },
      {
          'color': 'hsl(262, 52%, 47%)',
          'label': 'Deep Purple'
      },
      {
          'color': 'hsl(231, 48%, 48%)',
          'label': 'Indigo'
      },
      {
          'color': 'hsl(207, 90%, 54%)',
          'label': 'Blue'
      },
  ]

CKEDITOR_5_CONFIGS = {
'default': {
    'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

},
'extends': {
    'blockToolbar': [
        'paragraph', 'heading1', 'heading2', 'heading3',
        '|',
        'bulletedList', 'numberedList',
        '|',
        'blockQuote',
    ],
    'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
    'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable',],
    'image': {
        'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                    'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
        'styles': [
            'full',
            'side',
            'alignLeft',
            'alignRight',
            'alignCenter',
        ]
    },
    'table': {
        'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
        'tableProperties', 'tableCellProperties' ],
        'tableProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
    },
    'tableCellProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        }
    },
    'heading' : {
        'options': [
            { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
            { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
            { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
            { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
        ]
    }
},
'list': {
    'properties': {
        'styles': 'true',
        'startIndex': 'true',
        'reversed': 'true',
    }
}
}

from django.conf import settings  # use this import for sqlite3

# set settings yours database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # for sqlite3
        'NAME': settings.BASE_DIR / 'db.sqlite3',
        'USER': '',  # Not used with sqlite3.
        'PASSWORD': '',  # Not used with sqlite3.
        'HOST': '',  # Not used with sqlite3.
        'PORT': '',  # Not used with sqlite3.
    }
}

DEBUG = True
SECRET_KEY = ''  # Set secret key app

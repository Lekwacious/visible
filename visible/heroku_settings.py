from .settings import *
import os

# settings.py
import dj_database_url

# set default value
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
    }
}

# if environment variable present, it must be Heroku
if 'DATABASE_URL' in os.environ:
    # replace default with parsed value
    DATABASES['default'] = dj_database_url.config(ssl_require=True)

    import django_heroku
    django_heroku.settings(locals())
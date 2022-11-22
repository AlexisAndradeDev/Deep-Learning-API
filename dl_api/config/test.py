"""
Default settings for test environment.
"""
from .deployment import *

# Secret key for dev env
SECRET_KEY = '}uqmE!Vu/S^W@6zBBGRTom!Fdj[OqTmB^X$[Ivq{3mRNVm@jg@;ofS0ee;Elr#nzGy'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '/tests/test_db.sqlite3',
    }
}
"""
Default settings for test environment.
"""
from .deployment import *

# Secret key for dev env
SECRET_KEY = '}uqmE!Vu/S^W@6zBBGRTom!Fdj[OqTmB^X$[Ivq{3mRNVm@jg@;ofS0ee;Elr#nzGy'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'tests/integration/integration_test_db.sqlite3',
    }
}

PRIVATE_STORAGE_ROOT = BASE_DIR / 'tests/integration/private_storage'
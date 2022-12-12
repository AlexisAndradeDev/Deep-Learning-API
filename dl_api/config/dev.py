"""
Default settings for development environment.
"""
from .deployment import *

# Secret key for dev env
SECRET_KEY = 'KPd_qYHot|VfA)_41vnW$fpr8r(H7+L@WA3gv^aZ;:Xc}z7xe$ql^#F*P04D6}k^#?'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dev' / 'dev_db.sqlite3',
    }
}

PRIVATE_STORAGE_ROOT = BASE_DIR / 'dev' / 'private_storage'

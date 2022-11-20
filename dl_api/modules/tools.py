from time import time
from django.utils.text import slugify

def generate_unique_id(str_):
    """
    Generates a unique ID using the current time and a string.

    Returns:
        str: Unique ID.
    """        
    strtime = ''.join(str(time()).split('.'))
    unique_id = f'{strtime[7:]}-{str_[:7]}'
    unique_id = slugify(unique_id)
    return unique_id

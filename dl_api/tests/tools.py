from datetime import datetime, date
from django.conf import settings

def setUpCatsAndDogsDatasetTest(testCase):
    testCase.dataset_name = 'Cats and dogs'
    testCase.dataset_public_id = ''
    testCase.dataset_root_dir = settings.BASE_DIR / 'testing/data/cats_and_dogs/'
    testCase.classes = {'cats': {}, 'dogs': {}}

def dateIsToday(date_str):
    """
    Args:
        date_str (str): Date.
            Format: '%Y-%m-%d'
    Returns:
        bool: True if date_str parsed as a date is the same date as today.
    """
    date_ = datetime.strptime(date_str, r'%Y-%m-%d').date()
    return date_ == date.today()
        

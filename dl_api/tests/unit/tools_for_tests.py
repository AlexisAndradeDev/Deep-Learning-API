import os
from datetime import datetime, date
from django.conf import settings

def set_up_cats_and_dogs_dataset_test(testCase):
    testCase.dataset_name = 'Cats and dogs'
    testCase.dataset_public_id = ''
    testCase.dataset_root_dir = settings.BASE_DIR / 'testing/data/cats_and_dogs/'
    testCase.expected_classes = {'cat': {}, 'dog': {}}

def date_is_today(date_str):
    """
    Args:
        date_str (str): Date.
            Format: '%Y-%m-%d'
    Returns:
        bool: True if date_str parsed as a date is the same date as today.
    """
    date_ = datetime.strptime(date_str, r'%Y-%m-%d').date()
    return date_ == date.today()

def check_if_dataset_root_dir_exists(dataset_public_id):
    dataset_root_dir = settings.PRIVATE_STORAGE_ROOT / f'datasets/{dataset_public_id}'
    return os.path.isdir(dataset_root_dir)

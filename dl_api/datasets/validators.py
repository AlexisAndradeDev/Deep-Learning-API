from rest_framework.validators import ValidationError

def validate_classes(value):
    if not isinstance(value, list):
        raise ValidationError('\'classes\' must be a list.')
    
    classes = value
    for class_ in value:
        if not isinstance(class_, str):
            raise ValidationError(f'Invalid class name \'{class_}\': expected a string.')

        MAX_LENGTH = 30
        if len(class_) > MAX_LENGTH:
            raise ValidationError(f'Invalid class name \'{class_}\': length must not be greater than {MAX_LENGTH}.')
        
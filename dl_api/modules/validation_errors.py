from rest_framework.validators import ValidationError

class FieldValidationError(ValidationError):
    """
    Validation exception for fields in request JSON objects.
    
    This exception is raised when a validation error occurs in a field of a
    request JSON object.
    """
    def __init__(self, field_name, detail=None, code=None):
        """
        Initialize a FieldValidationError instance with the specified
        field name, error detail and error code.
        
        Args:
            field_name: The name of the field that failed validation.
            detail: Optional error detail for the exception.
            code: Optional error code for the exception.
        
        Raises:
            TypeError: If field_name is not a string.
        """
        if not isinstance(field_name, str) and field_name is not None:
            raise TypeError(f'Field name must be a string.')

        self.field_name = field_name
        self.detail_str = detail
        self.update_detail_str()

        super().__init__(self.detail_str, code)
    
    def update_detail_str(self):
        if self.detail_str:
            self.detail_str = f'Invalid field \'{self.field_name}\': {self.detail_str}.'
        else:
            self.detail_str = f'Invalid field \'{self.field_name}\'.'
    
class ContainerFieldValidationError(FieldValidationError):
    """
    Validation exception for fields that contain other fields.
    
    This class is raised when there is a validation error in a nested field
    of a request JSON object. The details of the nested field are included 
    inside of the details of this field.
    """
    def __init__(self, field_name, contained_field_error, code=None):
        """
        Args:
            field_name: The name of the container field that failed validation.
            contained_field_error: The field validation error of the nested field.
            code: Optional error code for the exception.
        
        Raises:
            TypeError: If contained_field_error is not a FieldValidationError instance.
        """
        if not isinstance(contained_field_error, FieldValidationError):
            raise TypeError(f'Contained field exception must be a FieldValidationError.')
        
        self.contained_field_error = contained_field_error

        super().__init__(field_name, None, code)
    
    def update_detail_str(self):
        contained_field_detail = self.contained_field_error.detail_str

        if contained_field_detail[-1] == '.':
            # remove dot
            contained_field_detail = contained_field_detail[:-1]

        self.detail_str = f'\'{self.field_name}\' -> {contained_field_detail}.'

class TypeValidationError(FieldValidationError):
    """
    Validation exception for fields that have a specific type.
    
    This class is raised when a field in a request JSON object does not have
    any of the expected types.
    """
    def __init__(self, field_name, expected_types, code=None):
        """
        Args:
            field_name: The name of the field that failed validation.
            expected_types: A tuple of expected types for the field.
            code: Optional error code for the exception.
        
        Raises:
            TypeError: If expected_types is not a tuple of type instances.
        """

        if (not isinstance(expected_types, tuple) or
                not all(isinstance(expected_type, type) for expected_type in expected_types)):
            raise TypeError(f'expected_types must be a tuple of \'type\' objects.')

        detail = f'expected one of the following types {expected_types}\''
        super().__init__(field_name, detail, code)
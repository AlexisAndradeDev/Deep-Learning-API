from rest_framework.exceptions import ValidationError
# import tensorflow.keras.losses as losses
from modules.validation_errors import FieldValidationError, ContainerFieldValidationError, TypeValidationError

LAYER_TYPE_FIELDS = {
    'Input': ['shape'],
    'Dense': ['units'],
    'MaxPool2D': ['pool_size', 'strides', 'padding'],
    'Flatten': [],
    'Conv2D': ['filters', 'kernel_size'],
}

LAYER_TYPE_OPTIONAL_FIELDS = {
    'Dense': ['activation'],
    'Conv2D': ['strides', 'padding', 'activation'],
}

ALLOWED_CATEGORIES_TYPES = {
    'input': ['Input'],
    'hidden': ['Conv2D', 'MaxPool2D', 'Flatten', 'Dense'],
    'output': ['Dense'],
}

ACTIVATIONS = [
    'elu', 'exponential', 'gelu', 'hard_sigmoid', 'linear', 'relu', 'selu', 
    'sigmoid', 'softmax', 'softplus', 'softsign', 'swish', 'tanh',
]

FRAMEWORKS = ['tf']

def validate_from_logits(value):
    if not isinstance(value, bool):
        raise TypeValidationError('activation', bool)

LOSSES = {
    'BinaryCrossentropy': {
        'from_logits': validate_from_logits,
    },
}

def validate_name(value):
    field_name = 'name'

    if not isinstance(value, str):
        raise FieldValidationError(field_name, 'must be a string')
    
    if not 3 <= len(value) <= 50:
        raise FieldValidationError(field_name, f'length must be between 3 and 50 characters')

def validate_framework(value):
    field_name = 'framework'

    if not isinstance(value, str):
        raise FieldValidationError(field_name, 'must be a string')
    
    if value not in FRAMEWORKS:
        raise FieldValidationError(field_name, f'expected one of {FRAMEWORKS}')

def validate_activation_layer_field(value, layer_name):
    field_name = 'activation'

    if not isinstance(value, str):
        raise TypeValidationError(field_name, (str,))
    
    if value not in ACTIVATIONS:
        raise FieldValidationError(field_name, f'expected one of {ACTIVATIONS}')

def validate_units_layer_field(value, layer_name):
    field_name = 'units'

    if not isinstance(value, int):
        raise TypeValidationError(field_name, (int,))
    
    if value <= 0:
        raise FieldValidationError(field_name, 'must be greater than 0')

def validate_shape_layer_field(value, layer_name):
    field_name = 'shape'

    if not isinstance(value, (list, tuple)) or not all(isinstance(i, int) for i in value):
        raise TypeValidationError(field_name, (list, tuple))

    if not all(i > 0 for i in value):
        raise FieldValidationError(field_name, 'all dimensions must be greater than zero')

def validate_filters_layer_field(value, layer_name):
    field_name = 'filters'

    if not isinstance(value, int):
        raise TypeValidationError(field_name, (int,))
    
    if value <= 0:
        raise FieldValidationError(field_name, 'must be positive')

def validate_kernel_size_layer_field(value, layer_name):
    field_name = 'filters'

    if not isinstance(value, (list, tuple)):
        raise TypeValidationError(field_name, (list, tuple))
    
    if len(value) != 2:
        raise FieldValidationError(field_name, 'expected a list or tuple with 2 elements')
    
    if not all(isinstance(i, int) for i in value):
        raise FieldValidationError(field_name, 'expected a list of int')
    
    if not all(i > 0 for i in value):
        raise FieldValidationError(field_name, 'expected positive integers')

def validate_strides_layer_field(value, layer_name):
    field_name = 'strides'

    if not isinstance(value, (list, tuple)):
        raise TypeValidationError(field_name, (list, tuple))
    
    if len(value) != 2:
        raise FieldValidationError(field_name, 'expected a list or tuple with 2 elements')
    
    if not all(isinstance(i, int) for i in value):
        raise FieldValidationError(field_name, 'expected a list of int')
    
    if not all(i > 0 for i in value):
        raise FieldValidationError(field_name, 'expected positive integers')

def validate_padding_layer_field(value, layer_name):
    field_name = 'padding'

    if not isinstance(value, str):
        raise FieldValidationError(field_name=field_name, detail='expected a string')

    valid_values = ['valid', 'same']
    if value not in valid_values:
        raise FieldValidationError(field_name=field_name, detail=f'expected one of {valid_values}')

def validate_architecture(value):
    field_name = 'architecture'
    if not isinstance(value, dict):
        raise FieldValidationError(field_name, 'must be a dictionary')
    
    try:
        for layer_name, layer_data in value.items():
            try:
                if not isinstance(layer_data, dict):
                    raise FieldValidationError(layer_name, 'must be a dictionary')
                
                if 'layer_category' not in layer_data:
                    raise FieldValidationError('layer_category', 'missing required field')
                
                if 'type' not in layer_data:
                    raise FieldValidationError('type', 'missing required field')
                
                layer_category = layer_data['layer_category']
                layer_type = layer_data['type']

                if layer_category not in ALLOWED_CATEGORIES_TYPES:
                    raise FieldValidationError('layer_category', f'expected one of {list(ALLOWED_CATEGORIES_TYPES.keys())}')
                
                if layer_type not in ALLOWED_CATEGORIES_TYPES[layer_category]:
                    raise FieldValidationError('type', f'expected one of {ALLOWED_CATEGORIES_TYPES[layer_category]} for layer category \'{layer_category}\'')

                if layer_type not in LAYER_TYPE_FIELDS:
                    raise FieldValidationError('type', 'unknown layer type')
                
                required_fields = LAYER_TYPE_FIELDS[layer_type]
                for field in required_fields:
                    if field not in layer_data:
                        raise FieldValidationError(field, 'missing required field')
                
                optional_fields = LAYER_TYPE_OPTIONAL_FIELDS.get(layer_type, [])
                
                allowed_fields = required_fields + optional_fields
                for field in layer_data:
                    if field not in allowed_fields and field not in ['layer_category', 'type']:
                        raise FieldValidationError(field, f'field not allowed for layer type \'{layer_type}\'')

                if 'activation' in layer_data:
                    activation = layer_data['activation']
                    validate_activation_layer_field(activation, layer_name)

                if 'units' in layer_data:
                    units = layer_data['units']
                    validate_units_layer_field(units, layer_name)
                
                if 'shape' in layer_data:
                    shape = layer_data['shape']
                    validate_shape_layer_field(shape, layer_name)

                if 'filters' in layer_data:
                    filters = layer_data['filters']
                    validate_filters_layer_field(filters, layer_name)
                
                if 'kernel_size' in layer_data:
                    kernel_size = layer_data['kernel_size']
                    validate_kernel_size_layer_field(kernel_size, layer_name)
                
                if 'strides' in layer_data:
                    strides = layer_data['strides']
                    validate_strides_layer_field(strides, layer_name)
                
                if 'padding' in layer_data:
                    padding = layer_data['padding']
                    validate_padding_layer_field(padding, layer_name)

            except FieldValidationError as e:
                raise ContainerFieldValidationError(layer_name, e)

    except FieldValidationError as e:
        raise ContainerFieldValidationError(field_name, e)

# def validate_loss_function(value):
#     if not isinstance(value, dict):
#         raise ValidationError(f'\'loss_function\' must be a dictionary.')    

#     try:
#         loss_function = losses.get(value)
#     except ValueError:
#         raise ValidationError(f'Invalid \'class_name\': expected one of ')
    
#     if value not in LOSS_FUNCTIONS:
#         raise ValidationError(f'\'Invalid field \'loss_function\': expected one of {LOSS_FUNCTIONS}')

# def validate_optimizer(value):
#     if not isinstance(value, str):
#         raise ValidationError(f'\'optimizer\' must be a string.')
    
#     if value not in OPTIMIZERS:
#         raise ValidationError(f'\'Invalid field \'optimizer\': expected one of {OPTIMIZERS}')


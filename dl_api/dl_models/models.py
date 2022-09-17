from django.db import models
from django.core.validators import MinLengthValidator

def model_file_path(instance, filename):
    return f'models/{instance.public_id}.npy'

class DLModel(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    public_id = models.SlugField(unique=True, max_length=18)
    file = models.FileField(upload_to=model_file_path)
    create_time = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.public_id}"

from django.db import models
from django.core.validators import MinLengthValidator

from modules.tools import generate_unique_id

# Create your models here.

class Dataset(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    public_id = models.SlugField(db_index=True, unique=True, max_length=18)
    classes = models.JSONField(default=dict)
    path = models.CharField(max_length=300)
    create_time = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.public_id}'

    def delete(self):
        # ! DELETE DATASET IMAGES
        super(Dataset, self).delete()

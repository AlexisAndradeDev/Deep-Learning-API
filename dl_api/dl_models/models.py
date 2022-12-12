from django.db import models
from django.core.validators import MinLengthValidator
from datasets.models import Dataset

class DLModel(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    public_id = models.SlugField(db_index=True, unique=True, max_length=18)
    datasets = models.ManyToManyField(Dataset, through='DLModelDataset')
    framework = models.CharField(max_length=12) # tf, pytorch, ...
    loss_function = models.CharField(max_length=35)
    optimizer = models.CharField(max_length=15)
    architecture = models.JSONField(default=dict)
    path = models.CharField(max_length=300)
    weights_path = models.CharField(max_length=300)
    create_time = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.public_id}"

class DLModelDataset(models.Model):
    dlmodel = models.ForeignKey(DLModel, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)

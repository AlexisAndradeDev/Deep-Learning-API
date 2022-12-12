from rest_framework import serializers

from .models import Dataset
from .validators import validate_classes

class DatasetCreateSerializer(serializers.ModelSerializer):
    classes = serializers.JSONField(required=False, validators=[validate_classes])

    class Meta:
        model = Dataset
        fields = [
            'name',
            'classes',
        ]

class DatasetCreateClassSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length=30, write_only=True)

class DatasetUploadClassSubsetSerializer(serializers.Serializer):
    subset_name = serializers.CharField(max_length=10)
    class_name = serializers.CharField(max_length=30, write_only=True)

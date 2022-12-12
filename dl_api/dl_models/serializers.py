from rest_framework import serializers

from .models import DLModel
from .validators import validate_name, validate_framework, validate_architecture
from modules.abstract_serializers import ReadOnlySerializer

class DLModelCreateSerializer(serializers.Serializer):
    name = serializers.CharField(validators=[validate_name])
    public_id = serializers.CharField(read_only=True)
    framework = serializers.CharField(validators=[validate_framework])
    # loss_function = serializers.CharField()
    # optimizer = serializers.CharField()
    architecture = serializers.JSONField(validators=[validate_architecture])
    create_time = serializers.DateField(read_only=True)
    last_modified = serializers.DateField(read_only=True)

class DLModelGetSerializer(ReadOnlySerializer):
    class Meta:
        model = DLModel
        fields = [
            'name',
            'public_id',
            'framework',
            'loss_function',
            'optimizer',
            'architecture',
            'create_time',
            'last_modified',
        ]

# class DLModelFitSerializer(serializers.ModelSerializer):
# 
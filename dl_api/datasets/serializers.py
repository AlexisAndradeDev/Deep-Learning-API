from rest_framework import serializers

from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'name',
            'public_id',
            'classes',
            'create_time',
            'last_modified',
        ]
        extra_kwargs = {
            'public_id': {'read_only': True},
            'classes': {'read_only': True},
            'create_time': {'read_only': True},
            'last_modified': {'read_only': True},
        }

    public_id = serializers.CharField(required=False)

class DatasetUploadClassSetSerializer(serializers.Serializer):
    set_name = serializers.CharField(max_length=10)
    class_name = serializers.CharField(max_length=30, write_only=True)

class DatasetCreateClassSerializer(serializers.Serializer):
    class_name = serializers.CharField(max_length=30, write_only=True)

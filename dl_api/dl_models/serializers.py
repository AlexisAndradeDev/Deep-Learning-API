from rest_framework import serializers

from .models import DLModel

class DLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DLModel
        fields = [
            'name',
            'public_id',
            'create_time',
            'last_modified',
        ]
        extra_kwargs = {
            'public_id': {'read_only': True},
            'create_time': {'read_only': True},
            'last_modified': {'read_only': True},
        }
    
    public_id = serializers.CharField(required=False)

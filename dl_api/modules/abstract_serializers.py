from rest_framework import serializers

class ReadOnlySerializer(serializers.Serializer):
    def get_fields(self):
        fields = super().get_fields()
        for field in fields:
            fields[field].read_only = True
        return fields
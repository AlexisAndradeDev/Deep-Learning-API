from django.conf.global_settings import MEDIA_ROOT
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from .models import DLModel

from .serializers import DLModelSerializer
from modules.tools import generate_unique_id

class ModelCreate(CreateAPIView):
    queryset = DLModel.objects.all()
    serializer_class = DLModelSerializer

    def perform_create(self, serializer):
        model = DLModel(**serializer.validated_data)
        model.public_id = generate_unique_id(serializer.validated_data['name'])

        model_path = f'models/{model.public_id}.h5'
        with open(settings.PRIVATE_STORAGE_ROOT / model_path, 'w+') as f:
            f.write('')
            f.close()
        model.file = model_path

        serializer = self.serializer_class(model) # update serializer
        model.save()

class ModelGet(RetrieveAPIView):
    queryset = DLModel.objects.all()
    serializer_class = DLModelSerializer
    lookup_field = 'public_id'


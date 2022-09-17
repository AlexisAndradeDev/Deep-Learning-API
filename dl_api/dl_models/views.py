from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DLModel

from dl_api.settings import MEDIA_ROOT
from .serializers import DLModelSerializer
from modules.tools import generate_unique_id

class ModelCreate(CreateAPIView):
    queryset = DLModel.objects.all()
    serializer_class = DLModelSerializer

    def perform_create(self, serializer):
        public_id = generate_unique_id(serializer.validated_data['name'])
        model = DLModel(**serializer.validated_data)
        model.public_id = public_id

        model_data_path = f'models/{model.public_id}.h5'
        with open(MEDIA_ROOT / model_data_path, 'w+') as f:
            f.write('')
            f.close()
        model.file = model_data_path

        model.save()
        serializer.validated_data['public_id'] = model.public_id # return public id

class ModelGet(RetrieveAPIView):
    queryset = DLModel.objects.all()
    serializer_class = DLModelSerializer
    lookup_field = 'public_id'

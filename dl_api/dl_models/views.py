import os
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from .models import DLModel

from .serializers import DLModelCreateSerializer, DLModelGetSerializer
from modules.tools import generate_unique_id
from modules.files_management import delete_dir

class DLModelCreate(APIView):
    def post(self, request):
        serializer = DLModelCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dlmodel = DLModel(**serializer.validated_data)

        public_id = generate_unique_id(serializer.validated_data['name'])
        dlmodel.public_id = public_id

        # create model root dir
        model_folder = settings.PRIVATE_STORAGE_ROOT / f'models/{dlmodel.public_id}'
        os.mkdir(model_folder)
        dlmodel.path = model_folder

        # create weights file
        weights_path = model_folder / 'weights.h5'
        with open(weights_path, 'w') as f:
            pass
    
        dlmodel.weights_path = str(weights_path)

        dlmodel.save()
        serializer.validated_data['public_id'] = dlmodel.public_id
        serializer.validated_data['create_time'] = dlmodel.create_time
        serializer.validated_data['last_modified'] = dlmodel.last_modified
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DLModelGet(RetrieveAPIView):
    queryset = DLModel.objects.all()
    serializer_class = DLModelGetSerializer
    lookup_field = 'public_id'

class DLModelDelete(APIView):
    def delete(self, request, public_id):
        try:
            dlmodel = DLModel.objects.get(public_id=public_id)
        except DLModel.DoesNotExist as e:
            return Response(data={'error': f'Model with id \'{public_id}\' not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            delete_dir(dlmodel.path)
        except ValueError as e:
            return Response(data={'error': 'Model root dir not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        dlmodel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class DLModelFit(APIView):
#     def post(self, request, public_id):
#         serializer = 

#         try:
#             dlmodel = DLModel.objects.get(public_id=public_id)
#         except DLModel.DoesNotExist as e:
#             return Response(data={'error': f'Model with public id \'{public_id}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
        


import os
import magic
from PIL import Image
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from .models import Dataset
from .serializers import DatasetSerializer, DatasetCreateClassSerializer, DatasetUploadClassSetSerializer

from modules.tools import generate_unique_id
from modules.files_management import delete_dataset_files

class DatasetCreate(APIView):
    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dataset = Dataset(**serializer.validated_data)

        public_id = generate_unique_id(serializer.validated_data['name'])
        dataset.public_id = public_id

        # create dataset root dir
        path = settings.PRIVATE_STORAGE_ROOT / f"datasets/{dataset.public_id}"
        os.mkdir(path)
        dataset.path = str(path)

        dataset.save()
        serializer.validated_data['public_id'] = dataset.public_id
        serializer.validated_data['create_time'] = dataset.create_time
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DatasetGet(RetrieveAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    lookup_field = 'public_id'

class DatasetDelete(APIView):
    def delete(self, request, public_id):
        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(data={'error': f'Resource \'{public_id}\' not found.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(dataset.path)
            delete_dataset_files(dataset.path)
        except ValueError as e:
            return Response(data={'error': 'Dataset root dir not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        dataset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DatasetCreateClass(APIView):
    def post(self, request, public_id):
        serializer = DatasetCreateClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_name = request.data.get('class_name')

        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if dataset.classes.get(class_name) != None:
            return Response(data={'error': 'Class name already exists'}, status=status.HTTP_409_CONFLICT)
        
        class_dir = dataset.path + f'/{class_name}'

        try:
            os.mkdir(class_dir)
        except IOError as e:
            return Response(data={'error': f'Root folder for class {class_name} already exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # load classes list from JSON field
        classes = dataset.classes
        classes[class_name] = {
            'sets': {}
        }
        dataset.classes = classes

        dataset.save()
        response_data = {'classes': dataset.classes}
        return Response(data=response_data, status=status.HTTP_200_OK)

class DatasetUploadToClassSet(APIView):
    def post(self, request, public_id):
        serializer = DatasetUploadClassSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_name = request.data.get('class_name')
        set_name = request.data.get('set_name')

        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(data={'error': f'Dataset with public id {public_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        classes = dataset.classes
        class_ = classes.get(class_name)
        if not class_:
            return Response(data={'error': f'Class {class_name} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        sets = class_.get('sets')
        set_ = sets.get(set_name)

        try:
            images = request.FILES.getlist('images')
        except MultiValueDictKeyError as e:
            return Response(data={'images': 'Dataset images files are required'}, status=status.HTTP_400_BAD_REQUEST)

        class_dir = dataset.path + f'/{class_name}'
        set_dir = class_dir + f'/{set_name}'

        try:
            os.mkdir(set_dir)
        except FileExistsError as e:
            pass

        images_num = 0
        for file in images:
            if file.size > 4*1024*1024:
                return Response(data={'error': 'Image file too large (limit: 4 megabytes)'}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
            
            mime = magic.from_buffer(file.read(), mime=True)
            if mime not in ['image/png', 'image/jpeg']:
                return Response(data={'error': 'Upload a JPEG or PNG image'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            
            type_ = mime.split('/')[-1].upper()

            # save image
            file.seek(0)
            image = Image.open(file)

            file_path = set_dir + f'/{file.name}'

            try:
                image.save(file_path, type_)
                images_num += 1
            except OSError:
                if os.path.exists(file_path):
                    # even with an exception, Pillow sometimes writes a file
                    # that contains partial content
                    os.remove(file_path)
                return Response(data={'error': f'Image {file.name} could not be written. The image file may contain partial or invalid data. All the images before {file.name} were written.'}, status=status.HTTP_422_CONFLICT)
        
        set_ = {'images_num': images_num}
        sets[set_name] = set_
        class_['sets'] = sets
        classes[class_name] = class_
        dataset.classes = classes
        dataset.save()

        response_data = {'classes': dataset.classes}
        return Response(response_data, status=status.HTTP_200_OK)

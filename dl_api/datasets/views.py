import glob
import os
import magic
from PIL import Image
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset
from .serializers import DatasetCreateSerializer, DatasetCreateClassSerializer, DatasetUploadClassSubsetSerializer
from .tools import create_dataset_class

from modules.tools import generate_unique_id
from modules.files_management import delete_dir

class DatasetCreate(APIView):
    def post(self, request):
        serializer = DatasetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create dataset data
        serializer.validated_data['public_id'] = generate_unique_id(serializer.validated_data['name'])

        # Create dataset root dir
        path = settings.PRIVATE_STORAGE_ROOT / f"datasets/{serializer.validated_data['public_id']}"
        serializer.validated_data['path'] = str(path)
        os.mkdir(serializer.validated_data['path'])

        # Dataset classes
        # the classses field in the request contains a list of classes names
        # in the dataset model, this field is a dict
        classes = serializer.validated_data.pop("classes", [])
        serializer.validated_data['classes'] = {}
        for class_name in classes:
            try:
                create_dataset_class(
                    serializer.validated_data['classes'],
                    serializer.validated_data['path'], class_name,
                )
            except IOError as e:
                return Response(
                    data={'error': f'Root folder for class {class_name} already exists.'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Save dataset to the db
        try:
            dataset = Dataset(**serializer.validated_data)
            dataset.save()
        except Exception as e:
            delete_dir(serializer.validated_data['path'])
            raise e

        response_data = {
            'name': dataset.name,
            'public_id': dataset.public_id,
            'classes': dataset.classes,
            'create_time': dataset.create_time,
            'last_modified': dataset.last_modified,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

class DatasetGet(APIView):
    def get(self, request, public_id):
        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(data={'error': f'Dataset with public id \'{public_id}\' not found.'}, status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'name': dataset.name,
            'public_id': dataset.public_id,
            'classes': dataset.classes,
            'create_time': dataset.create_time,
            'last_modified': dataset.last_modified,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

class DatasetDelete(APIView):
    def delete(self, request, public_id):
        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(data={'error': f'Dataset with public id \'{public_id}\' not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            dataset.delete()
        except ValueError as e:
            return Response(data={'error': 'Dataset root directory not found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)

class DatasetCreateClass(APIView):
    def post(self, request, public_id):
        serializer = DatasetCreateClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_name = request.data.get('class_name')

        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(data={'error': f'Dataset with public id \'{public_id}\' not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if dataset.classes.get(class_name) != None:
            return Response(data={'error': f'Class name \'{class_name}\' already exists.'}, status=status.HTTP_409_CONFLICT)

        # Create class dir
        try:
            create_dataset_class(dataset.classes, dataset.path, class_name)
        except IOError as e:
            return Response(
                data={'error': f'Root folder for class \'{class_name}\' already exists.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ) # !

        dataset.save()
        response_data = {'classes': dataset.classes}
        return Response(data=response_data, status=status.HTTP_200_OK)

class DatasetUploadToClassSubset(APIView):
    def post(self, request, public_id):
        serializer = DatasetUploadClassSubsetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_name = request.data.get('class_name')
        subset_name = request.data.get('subset_name')

        try:
            dataset = Dataset.objects.get(public_id=public_id)
        except Dataset.DoesNotExist as e:
            return Response(data={'error': f'Dataset with public id \'{public_id}\' not found.'}, status=status.HTTP_404_NOT_FOUND)

        classes = dataset.classes
        class_ = classes.get(class_name)
        if not class_:
            return Response(data={'error': f'Class \'{class_name}\' does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            images = request.FILES.getlist('images')
        except MultiValueDictKeyError as e:
            return Response(data={'error': '\'images\' files are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if not images:
            return Response(data={'error': '\'images\' files list is empty. Make sure you sent correctly the files in the response.'}, status=status.HTTP_400_BAD_REQUEST)

        class_dir = dataset.path + f'/{class_name}'
        subset_dir = class_dir + f'/{subset_name}'

        try:
            os.mkdir(subset_dir)
        except FileExistsError as e:
            pass

        images_path = glob.glob(f'{subset_dir}/*.jpg') + glob.glob(f'{subset_dir}/*.png')
        images_num = len(images_path)

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

            file_path = subset_dir + f'/{file.name}'
            image_already_exists = os.path.isfile(file_path)

            try:
                image.save(file_path, type_)
                if not image_already_exists:
                    images_num += 1
            except OSError:
                if os.path.exists(file_path):
                    # even with an exception, Pillow sometimes writes a file
                    # that contains partial content
                    os.remove(file_path)
                return Response(data={'error': f'Image \'{file.name}\' could not be written. The image file may contain partial or invalid data. All the images before \'{file.name}\' were written.'}, status=status.HTTP_422_CONFLICT)
        
        subsets = class_.get('subsets')
        subset = {'images_num': images_num}
        subsets[subset_name] = subset

        class_['subsets'] = subsets
        classes[class_name] = class_
        dataset.classes = classes
        dataset.save()

        response_data = {'classes': dataset.classes}
        return Response(response_data, status=status.HTTP_200_OK)

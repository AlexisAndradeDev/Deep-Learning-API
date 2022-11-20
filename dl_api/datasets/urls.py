from django.urls import path
from . import views

urlpatterns = [
    path('create', views.DatasetCreate.as_view()),
    path('create-class/<slug:public_id>', views.DatasetCreateClass.as_view()),
    path('upload-set/<slug:public_id>', views.DatasetUploadToClassSet.as_view()),
    path('delete/<slug:public_id>', views.DatasetDelete.as_view()),
    path('get/<slug:public_id>', views.DatasetGet.as_view()),
]


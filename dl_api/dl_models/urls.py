from django.urls import path
from . import views

urlpatterns = [
    path('create', views.DLModelCreate.as_view()),
    path('get/<slug:public_id>', views.DLModelGet.as_view()),
    path('delete/<slug:public_id>', views.DLModelDelete.as_view()),
    # path('fit/<slug:public_id>', views.DLModelFit.as_view())
]

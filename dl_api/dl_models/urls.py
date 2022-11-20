from django.urls import path
from . import views

urlpatterns = [
    path('create', views.ModelCreate.as_view()),
    path('get/<slug:public_id>', views.ModelGet.as_view()),
    # path('train/<slug:public_id>', views.ModelTrain.as_view())
]

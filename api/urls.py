from django.urls import path

from . import views
from .views import ImageListCreateAPIView, ImageRetrieveDestroyAPIView

urlpatterns = [
    path('', ImageListCreateAPIView.as_view(), name='image-list-create'),
    path('<int:pk>/', ImageRetrieveDestroyAPIView.as_view(), name='image-retrieve-destroy'),
]
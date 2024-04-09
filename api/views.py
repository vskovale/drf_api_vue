from django.shortcuts import render

# Create your views here.
import json

from django.contrib.sites import requests
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics
from .models import Image
from .serializers import ImageSerializer


class ImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

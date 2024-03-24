from rest_framework import serializers
from .models import MyModel
from django.db import models
from .models import Video

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'my_field', 'another_field']  # Or list specific fields you want to include

class VideoUploadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    video = serializers.FileField()
    photo = serializers.ImageField()
    
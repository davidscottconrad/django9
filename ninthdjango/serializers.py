from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'my_field', 'another_field']  # Or list specific fields you want to include

class VideoUploadSerializer(serializers.Serializer):
    video = serializers.FileField()
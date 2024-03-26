from rest_framework import serializers
from .models import MyModel
from django.db import models
from .models import Video
from django.core.files.storage import default_storage

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'my_field', 'another_field']  # Or list specific fields you want to include

class VideoUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    video = serializers.FileField()
    photo = serializers.ImageField()
    
class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'name', 'description', 'video_file', 'photo_url']

    def get_video_file(self, obj):
        # Retrieve the video file from S3
        video_url = obj.video_url
        s3_key = video_url.split('?')[0].split('amazonaws.com/')[1]

        # Retrieve the video file from S3 using the S3 key
        video_file = default_storage.open(s3_key)
        return video_file
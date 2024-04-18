from rest_framework import serializers
from .models import MyModel
from django.db import models
from .models import Video
from .models import Thumbnails
from .models import VideoMetadata
from .models import Movies
from django.core.files.storage import default_storage
import logging
logger = logging.getLogger(__name__)
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
    video_file = serializers.SerializerMethodField(method_name='get_video_file')

    class Meta:
        model = Video
        fields = ['id', 'name', 'description', 'video_file', 'photo_url']

    def get_video_file(self, obj, video=True):
        # Retrieve the video file from S3
        video = self.context.get("video")
        logger.warning(f'serierlier video variable: {video}')

        if video is True:
            video_url = obj.video_url
            s3_key = video_url.split('?')[0].split('amazonaws.com/')[1]

            # Retrieve the video file from S3 using the S3 key
            video_file = default_storage.open(s3_key)
            return video_file
        if  video is False: 
            logger.warning('inside the false if')
            photo_url = obj.photo_url
            s3_key = photo_url.split('?')[0].split('amazonaws.com/')[1]

            # Retrieve the video file from S3 using the S3 key
            video_file = default_storage.open(s3_key)
          
            return video_file
    
    # def get_photo_file(self, obj):
    #     logger.warning(f'video objs',obj)
    #     # Retrieve the photo file from S3
    #     photo_url = obj.photo_url
    #     s3_key = photo_url.split('?')[0].split('amazonaws.com/')[1]
    #     # Retrieve the photo file from S3 using the S3 key
    #     photo_file = default_storage.open(s3_key)
    #     return photo_file

class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnails
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'

class VideoMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMetadata
        fields = ['id', 'name', 'description', 'video_key', 'photo_key']
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoUploadSerializer
from django.core.files.storage import default_storage
from .models import Video
import uuid

@api_view(['GET','POST'])
def upload_video(request):
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoUploadSerializer(videos, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            description = serializer.validated_data['description']
            video = serializer.validated_data['video']
            photo = serializer.validated_data['photo']

            video_url = upload_file_to_s3(video)
            photo_url = upload_file_to_s3(photo)

            # Save the video information to the database
            video_obj = Video(name=name, description=description, video_url=video_url, photo_url=photo_url)
            video_obj.save()

            return Response({'video_url': video_url, 'photo_url': photo_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_file_to_s3(file):
    file_extension = file.name.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"media/{unique_filename}"  # Update the file path as needed

    # Save the file to S3
    default_storage.save(file_path, file)

    # Get the URL of the uploaded file
    file_url = default_storage.url(file_path)

    return file_url
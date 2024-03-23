from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoUploadSerializer
from django.core.files.storage import default_storage
import uuid

@api_view(['POST'])
def upload_video(request):
    if request.method == 'POST':
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.validated_data['video']
            video_url = upload_file_to_s3(video)
            return Response({'video_url': video_url}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_file_to_s3(file):
    file_extension = file.name.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"videos/{unique_filename}"
    
    # Save the file to S3
    default_storage.save(file_path, file)
    
    # Get the URL of the uploaded file
    file_url = default_storage.url(file_path)
    
    return file_url
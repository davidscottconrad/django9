from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoUploadSerializer
from .serializers import VideoSerializer
from django.core.files.storage import default_storage
from .models import Video
import uuid
from django.http import HttpResponse
import logging
from rest_framework.parsers import MultiPartParser, FormParser
import base64
from django.http import JsonResponse
import json
logger = logging.getLogger(__name__)
@api_view(['GET','POST'])
# @parser_classes((MultiPartParser, FormParser))
def upload_video(request):
    if request.method == 'GET':
        video_id = request.query_params.get('id')
        # info = request.query_params.get('info')
        if video_id:
            logger.info('hitting if')
            try:
                video = Video.objects.get(id=video_id)
                logger.info(f"video id: {video}")
           
                serializer = VideoSerializer(video, context={'video': True})
                video_file = serializer.data['video_file']
                response = HttpResponse(video_file, content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{video.name}.mp4"'
                return response
            except Video.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
        else:
            logger.warning('Homepage was accessed at hours!')

            photo = Video.objects.first()
            # serializer = VideoSerializer(photo, context={'video': False})
            # photo_file = serializer.data['video_file']

            # # Encode the photo file content as base64
            # encoded_string = base64.b64encode(photo_file).decode("utf-8")

            # logger.warning(f"Photo file path/URL: {photo}")

            # response_data = {
            #     'photo': encoded_string,
            #     'filename': 'test.png',
            #     'content_type': 'image/png',
            #     'name' : photo.name,
            #     'description' : photo.description
            # }

            response = HttpResponse(json.dumps(photo), content_type='application/json')
            return response

            # video_list = []
            # for video_data in serializer.data:
            #     video = {
            #         'id': video_data['id'],
            #         'name': video_data['name'],
            #         'description': video_data['description'],
            #         'photo_url': video_data['photo_url'],
            #     }
            #     # video_file = serializer.data['video_file']
            #     response = HttpResponse(video_data['photo_url'], content_type='image/png')
            #     response['Content-Disposition'] = f'attachment; filename="test.jpg"'
        
                
            #     # video_list.append(video)
            #     video_list.append(response)
            #     break
            #     # logger.info(f"data: {video}")
            #     # photo_file = video.photo.file
            #     # response.content_type = 'multipart/mixed'
            #     # response.attach(photo_file.name, photo_file, 'image/png')
            # return Response(video_list)
        
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

def is_base64(data):
    try:
        # Attempt to decode the data using base64
        decoded_data = base64.b64decode(data)
        
        # Check if the decoded data is not empty and consists of valid characters
        return decoded_data and all(c in (string.ascii_letters + string.digits + '+/=')
                                    for c in decoded_data.decode('utf-8'))
    except Exception as e:
        # Decoding failed or data is not base64-encoded
        return False


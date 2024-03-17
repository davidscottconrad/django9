from django.http import HttpResponse
import boto3
from botocore.exceptions import ClientError
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from .serializers import VideoSerializer
from .models import Videos

@api_view(['GET'])
def get_videos(request):
    if request.method == 'GET':
        videos = Videos.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
def retrieve_video(request):
    if request.method == 'GET' and 'video_path' in request.GET:
        video_path = request.GET.get('video_path')

        # Create an S3 client
        s3 = boto3.client('s3')

        # Specify the bucket name and object key (file path)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        object_key = video_path

        try:
            # Get the video file from S3
            file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
            video_data = file_obj['Body'].read()

            # Return the video data as a Django response
            response = HttpResponse(video_data, content_type='video/mp4')
           # response['Content-Disposition'] = f'attachment; filename="{object_key.split("/")[-1]}"'
            return response

        except ClientError as e:
            # Handle any S3 errors
            return HttpResponse(f'Error retrieving video: {e.response["Error"]["Message"]}')

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def upload_video(request):
    if request.method == 'POST':
        # Get the video file from the request
        video_file = request.FILES.get('video')

        if video_file:
            # Create an S3 client
            s3 = boto3.client('s3')

            # Specify the bucket name and object key (file path)
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            object_key = video_file.name  # Use the video file name as the object key

            try:
                # Upload the video file to S3
                s3.upload_fileobj(video_file, bucket_name, object_key)

                # Create a new Videos object and save it to the database
                video = Videos.objects.create(
                    video=video_file,
                    title=request.data.get('title', ''),
                    description=request.data.get('description', ''),
                    s3_key=object_key
                )

                # Serialize the video object
                serializer = VideoSerializer(video)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ClientError as e:
                # Handle any S3 errors
                return Response(f'Error uploading video: {e.response["Error"]["Message"]}', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('No video file provided', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
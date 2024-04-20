from rest_framework import generics
from .models import Thumbnails, VideoMetadata
from .serializers import ThumbnailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
from botocore.client import Config
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def MovieUploadView(request):
    if request.method == 'GET':
        # Check if the 'id' parameter is provided
        video_metadata_id = request.GET.get('id')
        if video_metadata_id:
            try:
                video_metadata = VideoMetadata.objects.get(id=video_metadata_id)
                video_key = video_metadata.video_key
                if video_key:
                    # Initialize the S3 client
                    s3 = boto3.client('s3',
                                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                      region_name='us-east-2')

                    # Define the bucket name
                    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

                    # Generate a signed URL for the video
                    signed_url = s3.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': bucket_name,
                            'Key': video_key,
                            'ResponseContentType': 'video/mp4'
                        },
                        ExpiresIn=3600  # URL expires in 1 hour
                    )

                    # Return the signed URL in a JSON response
                    return JsonResponse({'signed_url': signed_url})
                else:
                    return JsonResponse({'error': 'Video not found for the provided ID'}, status=404)
            except VideoMetadata.DoesNotExist:
                return JsonResponse({'error': 'VideoMetadata not found'}, status=404)
        else:
            # Initialize the S3 client
            s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='us-east-2')

            # Define the bucket name
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME

            # List objects in the bucket
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix='videos/')

            # Initialize an empty list to hold video details
            videos = []

            # Iterate through the objects in the bucket
            for obj in response.get('Contents', []):
                # Get the key (path + file name) of the object
                key = obj['Key']

                # Generate a signed URL for the file
                signed_url = s3.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': key
                    },
                    ExpiresIn=3600  # URL expires in 1 hour
                )

                # Append the details of the video to the list
                videos.append({
                    'key': key,
                    'signed_url': signed_url
                })

            # Return the list of videos with their signed URLs in a JSON response
            return JsonResponse({
                'videos': videos
            })

    elif request.method == 'POST':
        # Access the uploaded video file from the request's FILES dictionary
        uploaded_file = request.FILES.get('video')
        if not uploaded_file:
            return JsonResponse({'error': 'No video file found'}, status=400)

        # Access the VideoMetadata ID from the request data
        video_metadata_id = request.data.get('id')
        if not video_metadata_id:
            return JsonResponse({'error': 'VideoMetadata ID not provided'}, status=400)

        try:
            video_metadata = VideoMetadata.objects.get(id=video_metadata_id)
        except VideoMetadata.DoesNotExist:
            return JsonResponse({'error': 'VideoMetadata not found'}, status=404)

        # Initialize the S3 client
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='us-east-2')

        # Define the bucket and the key (path + file name) for the video file
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        key = f'videos/{uploaded_file.name}'

        # Upload the video file to S3
        s3.put_object(Bucket=bucket_name, Key=key, Body=uploaded_file.read())

        # Generate a signed URL for the video file
        signed_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )

        # Update the VideoMetadata object with the signed URL
        video_metadata.video_key = key
        video_metadata.save()

        # Return the signed URL in the JSON response
        return JsonResponse({'signed_url': signed_url})

    # Return a 405 Method Not Allowed response if the request method is not POST or GET
    return JsonResponse({'error': 'Method not allowed'}, status=405)
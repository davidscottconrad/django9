from rest_framework import generics
from .models import Thumbnails
from .serializers import ThumbnailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
from botocore.client import Config
from django.conf import settings
@api_view(['GET', 'POST'])
def ThumbnailUploadView(request):
    if request.method == 'GET':
        # Handle fetching a list of all images
        # Initialize the S3 client
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name='us-east-2')

        # Define the bucket name
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='images/')

        # Initialize an empty list to hold image details
        images = []

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

            # Append the details of the image to the list
            images.append({
                'key': key,
                'signed_url': signed_url
            })

        # Return the list of images with their signed URLs in a JSON response
        return JsonResponse({
            'images': images
        })

    # Return a 405 Method Not Allowed response if the request method is neither POST nor GET

    
    elif request.method == 'POST':
                # Access the uploaded file from the request's FILES dictionary
        uploaded_file = request.FILES.get('image')
        if not uploaded_file:
            return JsonResponse({'error': 'No image file found'}, status=400)
        
        # Initialize the S3 client
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name='us-east-2')

        # Define the bucket and the key (path + file name) for the file
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        key = f'images/{uploaded_file.name}'

        # Upload the file to S3
        s3.put_object(Bucket=bucket_name, Key=key, Body=uploaded_file.read())

        # Generate a signed URL for the file
        signed_url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )

        # Return the signed URL in the JSON response
        return JsonResponse({
            'signed_url': signed_url
        })

    # Return a 405 Method Not Allowed response if the request method is not POST
    return JsonResponse({'error': 'Method not allowed'}, status=405)
from django.http import JsonResponse
from .models import VideoMetadata
from .serializers import VideoMetadataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import boto3
from django.conf import settings
import logging
@api_view(['GET', 'POST'])
def video_metadata_list(request):
    logger = logging.getLogger(__name__)
    if request.method == 'GET':
        photo_param = request.query_params.get('photo')
        if photo_param:
            items = VideoMetadata.objects.filter(photo_key__isnull=False).order_by('id')
            data = []
            for item in items:
                # Initialize the S3 client
                s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, region_name='us-east-2')
                
                # Generate a signed URL for the photo
                photo_signed_url = None
                if item.photo_key:
                    photo_signed_url = s3.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                            'Key': item.photo_key
                        },
                        ExpiresIn=3600  # URL expires in 1 hour
                    )
                
                # Generate a signed URL for the background
                background_signed_url = None
                if item.background_key:
                    background_signed_url = s3.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                            'Key': item.background_key
                        },
                        ExpiresIn=3600  # URL expires in 1 hour
                    )
                
                data.append({
                    'id': item.id,
                    'description': item.description,
                    'name': item.name,
                    'photo_url': photo_signed_url,
                    'background_url': background_signed_url
                })
            return JsonResponse(data, safe=False)
        else:
            items = VideoMetadata.objects.all()
            serializer = VideoMetadataSerializer(items, many=True)
            return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        return JsonResponse({'error': 'Removed For Production'}, status=405)
        serializer = VideoMetadataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return a 400 Bad Request response if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
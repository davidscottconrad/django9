from django.http import JsonResponse
from .models import VideoMetadata
from .serializers import VideoMetadataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def video_metadata_list(request):
    if request.method == 'GET':
        items = VideoMetadata.objects.all()
        serializer = VideoMetadataSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        serializer = VideoMetadataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return a 400 Bad Request response if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
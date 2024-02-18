from django.http import JsonResponse
from .models import MyModel
from .serializers import MyModelSerializer
from rest_framework.decorators import api_view

@api_view(['GET','POST'])
def list(request):
    if request.method == 'GET':
        items = MyModel.objects.all()
        serializer = MyModelSerializer(items, many=True) 
        return JsonResponse(serializer.data, safe=False) 
    # if request.method == 'POST':

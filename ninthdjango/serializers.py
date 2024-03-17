from rest_framework import serializers
from .models import MyModel
from .models import Videos
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'my_field', 'another_field']  # Or list specific fields you want to include
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ['id', 'title', 'description', 'uploaded_at', 's3_key']
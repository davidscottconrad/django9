"""
URL configuration for ninthdjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninthdjango import views
from ninthdjango import VideoView
from ninthdjango import ThumbnailView
from ninthdjango import VideoMetadataView
from ninthdjango import MovieView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('items', views.list),
    path('video/', VideoView.upload_video, name='video'),
    path('thumbnail/', ThumbnailView.ThumbnailUploadView, name='thumbnail-upload'),
    path('movie-upload/', MovieView.MovieUploadView, name='movie-upload'),
   
    path('video-metadata/', VideoMetadataView.video_metadata_list, name='video-metadata-list'),
]

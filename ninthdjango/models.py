from django.db import models

class MyModel(models.Model):
    my_field = models.CharField(max_length=100)
    another_field = models.IntegerField(default=0)

    def __str__(self):
        return self.my_field + ' ' + str(self.another_field)
    
class Video(models.Model):
    name = models.CharField(max_length=100000)
    description = models.TextField()
    video_url = models.URLField(max_length=100000)
    photo_url = models.URLField(max_length=100000)
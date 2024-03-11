from django.db import models
import os

class MyModel(models.Model):
    my_field = models.CharField(max_length=100)
    another_field = models.IntegerField(default=0)

    def __str__(self):
        return self.my_field + ' ' + str(self.another_field)
    
class Videos(models.Model):
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=2000, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    s3_key = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Replace spaces with underscores in the video filename
        self.video.name = self.video.name.replace(' ', '_')
        
        # Set the s3_key field to the modified video filename
        self.s3_key = self.video.name
        
        super().save(*args, **kwargs)
from django.db import models

class MyModel(models.Model):
    my_field = models.CharField(max_length=100)
    another_field = models.IntegerField(default=0)

    def __str__(self):
        return self.my_field + ' ' + str(self.another_field)
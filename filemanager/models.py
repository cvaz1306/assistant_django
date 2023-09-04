from django.db import models

#Models
class File(models.Model):
    file=models.FileField()
    name=models.TextField(max_length=50)

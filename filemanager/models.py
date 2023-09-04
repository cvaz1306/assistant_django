from django.db import models


class File(models.Model):
    file=models.FileField()
    name=models.TextField(max_length=50)

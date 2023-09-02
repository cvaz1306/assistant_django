from django.db import models

# Create your models here.
class message(models.Model):
    message=models.TextField(null=True)
    attatched_file=models.FileField(upload_to='/resources', null=True)
    filename=models.TextField(null=False, max_length=50)
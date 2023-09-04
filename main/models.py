from django.db import models

# Create your models here
class message(models.Model):
    message=models.TextField(null=True)
    attatched_file=models.FileField(upload_to='resources', null=True)
    filename=models.TextField(null=False, max_length=50)
    isServer=models.BooleanField(default=False)
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Define the upload directory as 'uploads/'
    def __str__(self):
        return self.file.name  # Return the file's name as the string representation

from django.db import models

# Create your models here.
class message(models.Model):
    message=models.TextField(null=True)
    attatched_file=models.FileField(upload_to='resources', null=True)
    filename=models.TextField(null=False, max_length=50)
    isServer=models.BooleanField(default=False)
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Define the upload directory as 'uploads/'
    app_label="filemanager"
    name="filemanager"
    # Optionally, you can add more fields to store additional information about the uploaded file.
    # For example, you might want to store the user who uploaded the file, timestamp, etc.

    def __str__(self):
        return self.file.name  # Return the file's name as the string representation

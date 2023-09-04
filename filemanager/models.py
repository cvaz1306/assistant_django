from django.db import models

# models.py


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Define the upload directory as 'uploads/'
    app_label="filemanager"
    name="filemanager"
    # Optionally, you can add more fields to store additional information about the uploaded file.
    # For example, you might want to store the user who uploaded the file, timestamp, etc.

    def __str__(self):
        return self.file.name  # Return the file's name as the string representation

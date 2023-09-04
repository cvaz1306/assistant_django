import json
from django.shortcuts import redirect, render
import base64
import io
from django.http import HttpResponse
import matplotlib.pyplot as plt
import urllib.parse  # Import urllib.parse instead of urllib3
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from . import models
from .forms import *
# In your Django view, use the `HttpResponse()` function to return the image file to the user
@csrf_exempt
def filemanager(request):
    a=""
    context={}
    return render(request, "filemanager.html", context)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Optionally, you can provide a success message here.
            return redirect('/filemanager')  # Redirect to the file manager page after successful upload

    return HttpResponse(status=400)  # Return an error response if the form is not valid
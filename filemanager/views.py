import json
from django.shortcuts import render
import base64
import io
from django.http import HttpResponse
import matplotlib.pyplot as plt
import urllib.parse  # Import urllib.parse instead of urllib3
from django.views.decorators.csrf import csrf_exempt
import numpy as np
# In your Django view, use the `HttpResponse()` function to return the image file to the user
@csrf_exempt
def filemanager(request):
    a=""

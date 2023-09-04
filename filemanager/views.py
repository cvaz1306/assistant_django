import json
import os
from django.shortcuts import get_object_or_404, redirect, render
import base64
import io
from django.http import HttpResponse, JsonResponse
import matplotlib.pyplot as plt
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from . import models

@csrf_exempt
def filemanager(request):
    a=""
    context={}
    return render(request, "filemanager.html", context)
def upload_file(request):
    if(request.method=="POST"):
        file=request.FILES['file']
        dbentry=models.File(file=file, name=file.name)
        dbentry.save()
        print(f"Saved file!")
    return JsonResponse({"sucess":True})  # Redirect to the file manager page after successful upload
def files(request):
    return JsonResponse(([{"name": file.file.name, "id":file.id} for file in models.File.objects.all()]), safe=False)
def getFile(request):
    #reqData=json.loads(request.body)
    reqId=request.GET.get('id',3)
    file_obj = get_object_or_404(models.File, id=reqId)

    try:
        # Check if the file exists
        if os.path.exists(file_obj.file.path):
            with open(file_obj.file.path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
                return response
    except: 
        return HttpResponse(status=404)
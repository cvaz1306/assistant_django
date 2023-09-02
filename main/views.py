from django.http import JsonResponse
from django.shortcuts import render
from . import texpprocessing
from . import models
# Create your views here.

def main(request):
    return render(template_name='main/main.html', request=request)

def mess(request):
    if(request.method=='POST' or request.method=="POST"):
        if(request.POST.get('message',None) is not None):
            message=request.POST.get('message',None)
            message=models.message(message=request.POST.get('message',None))
    return JsonResponse({message.message for message in models.message.objects.all()})
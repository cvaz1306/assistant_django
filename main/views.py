from django.http import JsonResponse
from django.shortcuts import render
from . import texpprocessing
from . import models
# Create your views here.

def main(request):
    return render(template_name='main/main.html', request=request)

def mess(request):
    return JsonResponse({message.message for message in models.message})
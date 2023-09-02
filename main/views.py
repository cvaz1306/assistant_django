from django.shortcuts import render
from . import texpprocessing
# Create your views here.

def main(request):
    return render(template_name='main/main.html', request=request)

def mess(request):
    
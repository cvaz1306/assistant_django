from django.http import JsonResponse
from django.shortcuts import render
from .texpprocessing import *
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def main(request):
    
    return render(template_name='main/main.html', request=request, context={'messages':models.message.objects.all()})
@csrf_exempt
def mess(request):
    x=intResp()
    postData=json.loads(request.body)
    print(f"Request method: {request.method}")
    print(str(request.body))
    if request.method == "POST":
        message = models.message(message=postData.get('message',None))
        message.save()
        print(f"Created Message: {message.message}")
        response=process("fff",input=postData.get('message',None))
        serverResponse=models.message(message=response, isServer=True)
        serverResponse.save()
        all_messages = {'messages':
            [
            {
                "message":message.message, 
                'filename':message.filename, 
                'isServer':message.isServer} 
            for message in models.message.objects.all()
            ],
            'response':response
            }
    print("Messed")
    return JsonResponse(all_messages, safe=False)
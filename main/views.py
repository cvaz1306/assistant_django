from django.http import JsonResponse
from django.shortcuts import render
from . import texpprocessing
from . import models
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def main(request):
    return render(template_name='main/main.html', request=request)
@csrf_exempt
def mess(request):
    postData=json.loads(request.body)
    print(f"Request method: {request.method}")
    print(str(request.body))
    if request.method == "POST":
        # Create a new message object and save it to the database
        message = models.message(message=postData.get('message',None))
        message.save()
        print(f"Created Message: {message.message}")

    # Retrieve all messages from the database and prepare them for JSON response
    all_messages = [{"message":message.message, 'filename':message.filename} for message in models.message.objects.all()]

    return JsonResponse(all_messages, safe=False)
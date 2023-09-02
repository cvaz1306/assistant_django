from django.http import JsonResponse
from django.shortcuts import render
from . import texpprocessing
from . import models
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def main(request):
    return render(template_name='main/main.html', request=request)
@csrf_exempt
def mess(request):
    print(f"Request method: {request.method}")
    if request.method == "POST":
        message_text = request.POST.get('message', None)
        print(f"Creating db entry: {message_text}")
        # Create a new message object and save it to the database
        message = models.message.objects.create(message=message_text)
        message.message=message_text
        message.save()

    # Retrieve all messages from the database and prepare them for JSON response
    all_messages = [message.message for message in models.message.objects.all()]

    return JsonResponse(all_messages, safe=False)
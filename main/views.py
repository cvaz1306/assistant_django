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
    if request.method == 'POST':
        message_text = request.POST.get('message', None)
        if message_text:
            # Create a new message object and save it to the database
            message = models.Message.objects.create(message=message_text)

    # Retrieve all messages from the database and prepare them for JSON response
    all_messages = [message.message for message in models.Message.objects.all()]

    return JsonResponse(all_messages, safe=False)
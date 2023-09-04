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
    postData=json.loads(request.body)
    # Create a simple plot
    equation = postData.get('equation','y=0')
    x = np.linspace(-2, 2, 100)
    
    y=eval(equation.replace('y=',''))
    try:
        ddd=""
    except:
        ddd=""
    # Create a figure and axes
    fig = plt.figure(figsize = (10, 5))
    # Create the plot
    plt.plot(x, eval("y"))    
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()  # Decode the base64 bytes to a string
    
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)  # Use urllib.parse instead of urllib3.parse
    html = '<img src="%s"/>' % uri
    return HttpResponse(html)

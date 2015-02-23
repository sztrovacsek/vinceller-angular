import logging
import json
import time

import time, os, base64, hmac, urllib
from hashlib import sha1

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import *

logger = logging.getLogger(__name__)


def api_user_info(request):
    data = {}
    data["response_to"] = "api_user_info"
    data["username"] = request.user.username
    data["logged_in"] = request.user.is_authenticated()
    return HttpResponse(
        json.dumps(data, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_wine_list(request):
    wines = Wine.objects.all()
    data = []
    for wine in wines:
        raw_wine_data = json.loads(wine.json)
        wine_data = {}
        wine_data["id"] =  wine.pk
        wine_data["name"] = raw_wine_data.get("name", "Sample wine")
        wine_data["description"] = \
            raw_wine_data.get("description", "Sample description")
        # assume it contains photo_url
        wine_data["photo_url"] = "{0}".format(raw_wine_data["photo_url"])
        wine_data["status"] = raw_wine_data.get("status", "available")
        if "genre" in raw_wine_data:
            wine_data["genre"] = raw_wine_data["genre"]
        data.append(wine_data)

    return HttpResponse(
        json.dumps(data, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    raw_wine_data = json.loads(wine.json)
    wine_data = raw_wine_data
    wine_data["id"] =  wine.pk
    wine_data["name"] = raw_wine_data.get("name", "Sample wine")
    wine_data["description"] = \
        raw_wine_data.get("description", "Sample description")
    # assume it contains photo_url
    wine_data["photo_url"] = "{0}".format(raw_wine_data["photo_url"])
    wine_data["status"] = raw_wine_data.get("status", "available")
    
    return HttpResponse(
        json.dumps(wine_data, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


"""
POST:{'age': '18',
 'bla': '(and some further information should come here)',
 'id': '18',
 'imageUrl': '/uploads/wine_photo_1.jpg',
 'name': 'Duennium 2010',
 'snippet': 'The best Hungarian wine ever'},

"""
@login_required
def api_wine_update(request):
    print("Request received: {0}".format(request.POST));
    data = request.POST
    wine_id = data["id"]
    if wine_id:
        wine = Wine.objects.filter(pk=int(wine_id)).first()
        if wine:
            print("Wine found: {0}".format(wine))
            wine.json = json.dumps(data)
            print("Wine updated: {0}".format(wine))
            wine.save()
    reply = {"reply": "OK",}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def api_sign_s3(request):
    print("Signing aws request")
    # Load necessary information into the application:
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    S3_BUCKET = 'vincang' 

    # Collect information on the file from the GET parameters of the request:
    mime_type = request.GET['s3_object_type']
    
    # Come up with a filename
    n = Wine.objects.count()
    object_name = 'wine_photo_{0}-{1}.jpg'.format(n+1, int(time.time()))

    # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
    expires = int(time.time()+10)
    amz_headers = "x-amz-acl:public-read"
 
    # Generate the PUT request that JavaScript will use:
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
     
    # Generate the signature with which the request can be signed:
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY.encode(), put_request.encode(), sha1).digest())
    # Remove surrounding whitespace and quote special characters:
    signature = urllib.parse.quote_plus(signature.strip())
    print("After composing signature: {0}".format(signature))

    # Build the URL of the file in anticipation of its imminent upload:
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    print("After composing url: {0}".format(url))

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url
    })
    print("After composing content: {0}".format(content))
    
    # Return the signed request and the anticipated URL back to the browser in JSON format:
    return HttpResponse(
        content,
        content_type='application/json'
    )


@login_required
@csrf_exempt
def api_wine_new(request):
    print("Request (add wine) received: {0}".format(request.POST));
    data = {} 
    data['photo_url'] = request.POST['avatar_url']
    wine = Wine(json=json.dumps(data))
    wine.save()
    print("Wine saved: {0}".format(wine.json));
    
    return redirect(reverse('index-view'))


@login_required
def raw_view(request):
    wines = Wine.objects.all()
    reply = []
    for wine in wines:
        data = json.loads(wine.json)
        url = data['photo_url']
        print("Wine: pk={0}, url= {1}".format(wine.pk, url))
        reply.append(data)
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['photo'])
            messages.info(request, "File upload was successful")
            return redirect(reverse('index-view'))
    else:
        form = UploadFileForm()

    return render(request, 'api/upload.html', {'form': form})


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    photo = forms.FileField(
        label=''
    )   
    photo.widget = forms.ClearableFileInput(
        attrs={'accept': 'image/*', 'class': 'btn btn-default'})


def handle_uploaded_file(f):
    n = Wine.objects.count()
    filename = 'wine_photo_{0}.jpg'.format(n+1)
    with open(settings.MEDIA_ROOT+'/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
   
    data = {} 
    data['photo_url'] = filename
    wine = Wine(json=json.dumps(data))
    wine.save()


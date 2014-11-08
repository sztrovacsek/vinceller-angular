import logging
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django import forms
from django.conf import settings
from .models import *

logger = logging.getLogger(__name__)


def api_wine_list(request):
    wines = Wine.objects.all()
    data = []
    for wine in wines:
        # assume it contains photo_url
        raw_wine_data = json.loads(wine.json)
        wine_data = {}
        wine_data["id"] =  wine.pk
        wine_data["name"] = raw_wine_data.get("name", "Sample wine")
        wine_data["description"] = \
            raw_wine_data.get("description", "Sample description")
        wine_data["photo_url"] = "{0}".format(raw_wine_data["photo_url"])
        data.append(wine_data)
    return HttpResponse(
        json.dumps(data, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def api_wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    raw_wine_data = json.loads(wine.json)
    wine_data = {}
    wine_data["id"] =  wine.pk
    wine_data["name"] = raw_wine_data.get("name", "Sample wine")
    wine_data["description"] = \
        raw_wine_data.get("description", "Sample description")
    # assume it contains photo_url
    wine_data["photo_url"] = "{0}".format(raw_wine_data["photo_url"])
    
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
@csrf_exempt
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
    reply = {"OK"}
    return HttpResponse(
        json.dumps(reply, sort_keys=True, separators=(',',':'), indent=4),
        content_type='application/json'
    )


def raw_view(request):
    wines = Wine.objects.all()
    for wine in wines:
        data = json.loads(wine.json)
        url = data['photo_url']
        wine.tmp_url = url
        print("Wine: pk={0}, url= {1}".format(wine.pk, url))
    return render(request, 'api/raw.html', {'wines': wines})


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


import logging
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django import forms
from django.conf import settings
from .models import *

logger = logging.getLogger(__name__)


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
            return redirect(reverse('raw'))
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


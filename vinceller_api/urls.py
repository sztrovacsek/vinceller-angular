from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from api.views import *
from client.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vinceller_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', index_view, name='index-view'),
    url(r'^$', RedirectView.as_view(url='/static/index2.html', permanent=False), name='index-view'),
    url(r'^raw$', raw_view, name='raw'),
    url(r'^upload/', upload_file_view, name='upload-file'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from api.views import *
from client.views import *

urlpatterns = patterns('',
    # Examples:

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', index_view, name='index-view'),
    # url(r'^$', RedirectView.as_view(url='/login/', permanent=False)),
    url(r'^login/$', auth_views.login,
        {'template_name': 'api/login.html'}),

    url(r'^$', RedirectView.as_view(url='app/index.html', permanent=False), name='index-view'),
    url(r'^raw$', raw_view, name='raw'),

    url(r'^api/wine_list$', api_wine_list, name='api-wine-list'),
    url(r'^api/wine_update$', api_wine_update, name='api-wine-update'),
    url(r'^api/wine_detail/(?P<wine_id>\d+)$', api_wine_detail, name='api-wine-detail'),

    url(r'^upload/', upload_file_view, name='upload-file'),
    url(r'^upload2/', api_wine_new, name='api-wine-add'),
    url(r'^sign_s3/', api_sign_s3, name='sign-s3'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



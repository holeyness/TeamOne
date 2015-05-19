# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from poster import views
from django.conf import settings
from django.conf.urls.static import static
from tastypie.api import Api
from poster.api import *

import html5_appcache
html5_appcache.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(PostResource())
v1_api.register(UserPostResource())

urlpatterns = patterns(
    '',
	url(r'^$', views.newsfeed, name='newsfeed'),
	url(r'^new/$', views.timefeed, name='timefeed'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^post/(?P<id>\d+)/$', views.singlepost, name='singlepost'),
    url(r'^like/$', views.like, name='like'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/v1/doc/',
      include('tastypie_swagger.urls', namespace='v1_api_tastypie_swagger'),
      kwargs={
          "tastypie_api_module":"poster.urls.v1_api",
          "namespace":"v1_api_tastypie_swagger",
          "version": "0.1"}
    ),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='login'),
    url(r'^signup/$', views.signup, name='login'),
    #url(r'^me/', views.me, name='me')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

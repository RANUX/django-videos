# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from djangovideos import views

urlpatterns = patterns('',
    url(r'^add_video/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/$',
        views.add_video, name='add_video'),
    url(r'^delete_video/(?P<video_pk>\d+)/$',
        views.delete_video, name='delete_video'),

)

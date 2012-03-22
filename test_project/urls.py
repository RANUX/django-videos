# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import pluggableapp
import views

urlpatterns = pluggableapp.patterns()

urlpatterns += patterns('',
        url('^$', views.add_form, name='index'),
        )

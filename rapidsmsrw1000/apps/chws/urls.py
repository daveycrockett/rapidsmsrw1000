#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
import chws.views as views

urlpatterns = patterns('',
    url(r'^chws$', views.view_uploads),
    url(r'^chws/import$', views.import_reporters_from_excell, name='import_chws'),
    url(r'^chws/pendings$', views.view_pendings, name='pendings'),
    url(r'^chws/confirms$', views.view_confirms, name='confirms'),
    url(r'^chws/view/errors/(?P<ref>\w+)$', views.errors, name='errors'),
    url(r'^chws/view/warnings/(?P<ref>\w+)$', views.warnings, name='warnings'),
    url(r'^chws/view/uploads$', views.view_uploads, name='uploads'),
    #url(r'^chws/download/list$', views.download_chws_list_template),
    
    
)


#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
import rapidsmsrw.1000.apps.webapp.views as views

urlpatterns = patterns('',
    url(r'^$',    views.home ),
    url(r'^ping$', views.check_availability),
    (r'^accounts/login/$', "rapidsmsrw1000.apps.webapp.views.login"),
    (r'^accounts/logout/$', "rapidsmsrw1000.apps.webapp.views.logout"),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^home/$',     views.dashboard),
    
    
)


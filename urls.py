# coding: utf-8
from django.conf.urls import patterns, include, url

#urlpatterns = patterns('',
#    url(r'^files/([0-9]{4})/([0-9]{2})/$', 'filemanager.views.list_requested'),
#)

urlpatterns = [
        url(r'^$', 'filemanager.views.list_current', name='list_current'),
        url(r'^scan/$', 'filemanager.views.scan_for_files', name='scan_for_files'),
        url(r'^(?P<year>[0-9]{4})/$', 'filemanager.views.list_by_date', name='list_by_date'),
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', 'filemanager.views.list_by_date', name='list_by_date'),
        url(r'^Video_SMI/$', 'filemanager.views.list_by_path', {'path': 'Video_SMI'}, name='list_by_path'),
        url(r'^delete/(?P<id>\d+)$', 'filemanager.views.delete_file'),
]

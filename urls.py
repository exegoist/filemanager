# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns( 'filemanager.views',
        url(r'^$', list_current, name='list_current'),
        url(r'^scan/$', scan_for_files, name='scan_for_files'),
        url(r'^(?P<year>[0-9]{4})/$', list_by_date, name='list_by_date'),
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', list_by_date, name='list_by_date'),
        url(r'^Video_SMI/$', list_by_path, {'path': 'Video_SMI'}, name='list_by_path'),
        url(r'^delete/(?P<id>\d+)$', delete_file),
)

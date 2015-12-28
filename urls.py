# coding: utf-8
from django.conf.urls import patterns, include, url
from filemanager import views as file_views

urlpatterns = [
        url(r'^$', file_views.list_current),
        url(r'^scan/$', file_views.scan_for_files),
        url(r'^(?P<year>[0-9]{4})/$', file_views.list_by_date),
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', file_views.list_by_date),
        url(r'^Video_SMI/$', file_views.list_by_path, {'path': 'Video_SMI'}),
        url(r'^delete/(?P<id>\d+)$', file_views.delete_file),
]

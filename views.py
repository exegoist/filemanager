# -*- coding: utf-8 -*-
""" view that handle files adding, listing, removing  """
import os
import collections
# import from django
from django.utils import timezone
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# import from filemanager
from .models import File
from .forms import FileForm

MONTHS = [('01','Січень'),
          ('02','Лютий'),
          ('03','Березень'),
          ('04','Квітень'),
          ('05','Травень'),
          ('06','Червень'),
          ('07','Липень'),
          ('08','Серпень'),
          ('09','Вересень'),
          ('10','Жовтень'),
          ('11','Листопад'),
          ('12','Грудень')]

MONTHS = collections.OrderedDict(MONTHS)


def year_urls(year, month):
    "function generating list of urls for years back and forward"
    return [(str(iyear) + '/' + month + '/', str(iyear), int(iyear) == int(year))
            for iyear in range(int(year)-1, int(year)+2)]

def month_urls(year, month):
    "function generating list of urls for month in current year"
    return [(year + '/' + month_order + '/', MONTHS[month_order], month_order == month)
            for n, month_order in list(enumerate(MONTHS))]

def list_universal(request, path, year, month):
    "function rendering list of uploaded files by path or year/month"
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = File(file=request.FILES['file'], file_path=path)
            instance.save()
            return HttpResponseRedirect('/' + path)
    else:
        form = FileForm()
    files = File.objects.filter(file_path=path)
    files_list = []
    for f in files:
        url = f.file.url
        name = f.file_name
        size = f.file.size
        delete_url = 'delete/' + str(f.id)
        files_list.append({'url':url, 'name':name, 'size':size, 'delete_url':delete_url})
    y_urls = year_urls(year, month)
    m_urls = month_urls(year, month)
    request.session.set_expiry(3600)
    return render_to_response('list.html',
                              {'files_list': files_list, 'form': form, 'year_urls': y_urls,
                               'month_urls': m_urls, 'year': year, 'mname': MONTHS[month]},
                              context_instance=RequestContext(request))

@login_required
def list_by_date(request, year=timezone.now().strftime('%Y'),
                 month=timezone.now().strftime('%m')):
    "gimme date i'l give you path"
    path = '{}/{}'.format(year,month)
    return list_universal(request, path, year, month)

@login_required
def list_by_path(request, path):
    "gimme path and go universal"
    return list_universal(request, path, timezone.now().strftime('%Y'),
                          timezone.now().strftime('%m'))

@login_required
def list_current(request):
    "list by current month"
    return list_by_path(request, '{}/{}'.format(timezone.now().strftime('%Y'),
                        timezone.now().strftime('%m')))

def scan_for_files(request):
    "scan directory for files and populate db with founded files"
    media_dir = '/media'
    video_dir = '/media/video'
    for root, dirs, files in os.walk(video_dir, topdown=True):
        for f in files:
            if not File.objects.filter(file_name=f):
                instance = File(file=os.path.join(root.replace(media_dir, ""), f)[1:],
                                file_name=f,
                                file_path=root.replace(video_dir, "")[1:])
                instance.save()
    return HttpResponseRedirect('/')

@login_required
def delete_file(request,id):
    instance = get_object_or_404(File, pk=id)
    instance.delete()
    return HttpResponseRedirect('/')

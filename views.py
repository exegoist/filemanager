# coding: utf-8
# import from python
import os
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

mnames = "Січень Лютий Березень Квітень Травень Червень Липень Серпень Вересень Жовтень Листопад Грудень"
mnames = mnames.split()

def year_urls(year, month):
    return [(str(iyear) + '/' + month + '/', str(iyear), int(iyear) == int(year)) for iyear in range(int(year)-1, int(year)+2)]

def month_urls(year, month):
    return [(str(year) + '/' + str(n+1).zfill(2) + '/', mname, n + 1 == int(month)) for n, mname in enumerate(mnames)]

def list_universal(request, path, year, month):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = File(file_object = request.FILES['file_object'], file_path = path)
            instance.save()
            return HttpResponseRedirect('/' + path)
    else:
        form = FileForm()
    files = File.objects.filter(file_path=path)
    files_list = []
    for file in files:
        furl = file.file_object.url
        fname = file.file_object.name[file.file_object.name.rfind('/')+1:]
        fsize = str(int(file.file_object.size/1048576)) + ' Mb'
        delete_url = 'delete/' + str(file.id)
        files_list.append({'url':furl, 'name':fname, 'size':fsize, 'delete_url':delete_url})
    y_urls = year_urls(year,month)
    m_urls = month_urls(year,month)
    request.session.set_expiry(3600)
    return render_to_response('list.html', {'files_list': files_list, 'form': form, 'year_urls': y_urls, 'month_urls': m_urls, 'year': year, 'mname': mnames[int(month)-1] }, context_instance=RequestContext(request))

@login_required
def list_by_date(request, year, month):
    path = year + '/' + month + '/'
    return list_universal(request, path, year, month)

@login_required
def list_by_path(request, path):
    return list_universal(request, path + '/', timezone.now().strftime('%Y'), timezone.now().strftime('%m'))

@login_required
def list_current(request):
    return list_by_path(request, timezone.now().strftime('%Y') + '/' + timezone.now().strftime('%m'))

def scan_for_files(request):
    curr_dir = '/media/video'
    for root, dirs, files in os.walk(curr_dir, topdown=True):
        for name in files:
            if len(File.objects.filter(Q(file_object__icontains = name), file_path = root[13:] + '/')) == 0:
                instance = File(file_object = os.path.join(root[7:], name), file_path = root[13:] + '/')
                instance.save()
    return HttpResponseRedirect('/')

def delete_file(request,id):
    instance = get_object_or_404(File, pk=id)
    instance.delete()
    return HttpResponseRedirect('/')

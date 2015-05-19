from django.contrib import admin
from filemanager.models import File
# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_filter = ['file_path']

admin.site.register(File,FileAdmin)

# -*- coding: utf-8 -*-
import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

def generate_path(instance, filename):
    " function for generating upload path "
    instance.file_name = filename
    return os.path.join('video/', instance.file_path, filename)

# Create your models here.
class File(models.Model):
    " class of files stored by filemanager "
    class Meta:
        " meta class attributes "
        db_table = 'files'
        ordering = ['-pk']

    file = models.FileField(upload_to=generate_path)
    file_name = models.CharField(max_length=60)
    file_path = models.CharField(max_length=30)
    def __unicode__(self):
        return self.file_name

@receiver(pre_delete, sender=File)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

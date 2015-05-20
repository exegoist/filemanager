# -*- coding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
class File(models.Model):
    class Meta:
        db_table = 'files'
        ordering = ['-pk']

    file_object = models.FileField(upload_to=lambda instance, filename: 'video/' + instance.file_path + filename)
    file_path   = models.CharField(max_length=30)
    def __unicode__(self):
        return self.file_object.name[self.file_object.name.rfind('/')+1:]

@receiver(pre_delete, sender=File)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file_object.delete(False)

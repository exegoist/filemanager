# -*- coding: utf-8 -*-
from django import forms

class FileForm(forms.Form):
    file_object = forms.FileField(label='Виберіть файл')

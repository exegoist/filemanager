### FILEMANAGER

Filemanager is a simple django app for uploading files to server. Interface uses Foundation css-framework
Works with django >= 1.8

# Installation:

1. clone app to Your project

    `git clone https://github.com/exegoist/filemanager.git`

2. add `filemanager` to tuple of installed apps in settings.py:

    '''
    INSTALLED_APPS = (
    ...
    'django.contrib.staticfiles',
    'filemanager',
    )
    '''

3. add MEDIA_ROOT in settings.py (directory, in which files will be stored), for example:

    '''
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    '''

4. add urlresolver into your project urls.py:

    '''
    url('r^', include('filemanager.urls')),
    '''
5. make migrations and start server.

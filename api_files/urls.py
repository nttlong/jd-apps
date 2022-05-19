from django.urls import path
from django.conf.urls import include, url
from . import views,upload,view_files,views_directory

urlpatterns = (
    url(r'(?P<app_name>[\w\-]+)/list', view_files.get_list, name='view_files.get_list'),
    url(r'(?P<app_name>[\w\-]+)/source/(?P<upload_id>[\w\-]+).*', views.source, name='source'),
    url(r'(?P<app_name>[\w\-]+)/directory/(?P<full_path>.*)$', views_directory.source, name='views_directory.source'),
    url(r'(?P<app_name>[\w\-]+)/upload/register$', upload.register, name='upload.register'),
    url(r'(?P<app_name>[\w\-]+)/upload/chunk$', upload.chunk, name='upload.chunk'),
)
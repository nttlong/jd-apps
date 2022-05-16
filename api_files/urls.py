from django.urls import path
from django.conf.urls import include, url
from . import views,upload

urlpatterns = (
    url(r'(?P<app_name>[\w\-]+)/source/(?P<upload_id>[\w\-]+).*', views.source, name='source'),
    url(r'(?P<app_name>[\w\-]+)/directory/(?P<full_path>.*)$', views.directory, name='unique_slug'),
    url(r'(?P<app_name>[\w\-]+)/registerupload$', upload.upload_register, name='unique_slug'),
)
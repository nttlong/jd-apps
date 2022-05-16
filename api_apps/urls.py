from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = (
    url(r'register', views.create_app, name='create_app'),
    url(r'list', views.list_apps, name='list_app'),
)
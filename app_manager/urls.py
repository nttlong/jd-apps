from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
import web.settings
import os
urlpatterns = [
    path('', views.index, name='index')

]
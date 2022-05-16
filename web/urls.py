"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,re_path
from django.urls import include, path,URLPattern
import ReEngine

import api_files.urls
urlpatterns = [
    path(r'admin/',admin.site.urls)
]

#
for app_name in ReEngine.info["APPS"].keys():
    try:
        urlpatterns.append(
           path(ReEngine.info["APPS"][app_name],include("{}.urls".format(app_name)))
        )
    except Exception as e:
        print(f"load url of {app_name} is fail {e}")
# handler404 = 'icase.views.icase_404_handler'

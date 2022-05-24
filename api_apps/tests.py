import datetime

from django.test import TestCase
import api_models.ModelApps
fx= api_models.ModelApps.sys_applications.Name!="Code"
where =api_models.ModelApps.sys_applications.RegisteredOn==datetime.datetime.now()
where =  where & fx
print(where)
# Create your tests here.

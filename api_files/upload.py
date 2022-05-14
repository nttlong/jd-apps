from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
@require_http_methods(["POST"])
def upload_register(request,app_name,upload_id):
    return HttpResponse("Xem hoac tai noi dung {} cua app {}".format(
        upload_id,
        app_name
    ))
@require_http_methods(["GET"])
def directory(request,full_path):
    return  HttpResponse("Xem hoac tai noi dung {}".format(full_path))
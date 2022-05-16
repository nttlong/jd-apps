from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import ReCompact.dbm.DbObjects
import api_models.ModelApps
from django.http import JsonResponse

# Create your views here.
@require_http_methods(["POST"])
def create_app(*args, **kwargs):
    print(args)
    pass


@require_http_methods(["POST"])
def list_apps(request):
    import ReCompact.db_context
    db = ReCompact.db_context.get_db()
    agg = ReCompact.dbm.DbObjects.aggregrate(db, api_models.ModelApps.sys_applications)

    return JsonResponse(list(agg), safe=False)

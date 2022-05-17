from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import ReCompact.dbm.DbObjects
import api_models.ModelApps
from django.http import JsonResponse
import ReCompact.auth as rpt_auth
# Create your views here.
@require_http_methods(["POST"])
def create_app(*args, **kwargs):
    print(args)
    pass


@require_http_methods(["POST"])
@rpt_auth.validator()
def list_apps(request,app_name):
    if app_name =='admin' and request.current_user:
        import ReCompact.db_context
        db = ReCompact.db_context.get_db()

        agg = ReCompact.dbm.DbObjects.aggregrate(db, api_models.ModelApps.sys_applications)
        agg=agg.sort(
            ReCompact.dbm.DbObjects.FIELDS.Name.asc(),
            ReCompact.dbm.DbObjects.FIELDS.Domain.asc(),
        )

        return JsonResponse(list(agg), safe=False)
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import ReCompact.db_context
import api_models.Model_Files
from django.http import JsonResponse
@require_http_methods(["POST"])
def get_list(request,app_name):
    import ReCompact.db_context
    db = ReCompact.db_context.get_db(app_name)


    agg = ReCompact.dbm.DbObjects.aggregrate(db, api_models.Model_Files.DocUploadRegister)
    agg = agg.sort(
        ReCompact.dbm.DbObjects.FIELDS.RegisteredOn.asc(),
        ReCompact.dbm.DbObjects.FIELDS.Name.asc(),
    )
    ret_list = list(agg)
    ret=[]
    for x in ret_list:
        ret+=[
            dict(
                FileName=x["FileName"],
                FileExt =x ["FileExt"],
                MimeType =x.get("MimeType",None),
                RegisterOn =x ["RegisterOn"],
                SizeInHumanReadable =x["SizeInHumanReadable"],
                UrlOfServerPath =f"{request._current_scheme_host}/api/files/{app_name}/directory/{x['FullFileName']}"
            )
        ]

    return JsonResponse(ret, safe=False)


# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import ReCompact.db_context
import api_models.Model_Files
import ReCompact.api_input
from django.http import JsonResponse,HttpResponse

class Filter:
    PageSize= (int,False)
    PageIndex = (int,False)

@ReCompact.api_input.map_param(cls_params=Filter)
@require_http_methods(["POST"])
def get_list(request,app_name,data:Filter,error:ReCompact.api_input.Error):

    if error:
        return error.to_error_500()

    if data is None:
        data= Filter()
        data.PageIndex=0
        data.PageSize=50
    if data.PageSize is None:
        data.PageSize=50
    if data.PageIndex is None:
        data.PageIndex=0
    import ReCompact.db_context
    import mimetypes
    import ReCompact.dbm

    db = ReCompact.db_context.get_db(app_name)


    agg = ReCompact.dbm.DbObjects.aggregrate(db, api_models.Model_Files.DocUploadRegister)
    agg = agg.sort(
        ReCompact.dbm.DbObjects.FIELDS.RegisteredOn.asc(),
        ReCompact.dbm.DbObjects.FIELDS.Name.asc(),
    ).skip(data.PageSize*data.PageIndex).limit(data.PageSize)
    ret_list = list(agg)
    ret=[]
    for x in ret_list:
        if x.get("MimeType",None) is None:
            ReCompact.dbm.DbObjects.update(
                db,
                api_models.Model_Files.DocUploadRegister,
                ReCompact.dbm.DbObjects.FILTER.FileName==x["FileName"],
                ReCompact.dbm.SET(
                    ReCompact.dbm.DbObjects.FIELDS.MimeType==mimetypes.guess_type(x["FileName"])[0]
                )
            )
        ret+=[
            dict(
                Status =x.get("Status",0),
                FileName=x.get("FileName",None),
                FileExt =x.get("FileExt",None),
                MimeType =x.get("MimeType",mimetypes.guess_type(x.get("FileName","a.dat"))[0]),
                RegisterOn =x.get("RegisterOn",None),
                SizeInHumanReadable =x.get("SizeInHumanReadable",None),
                UrlOfServerPath =f"{request._current_scheme_host}/api/files/{app_name}/directory/{x.get('FullFileName',None)}"
            )
        ]

    return JsonResponse(ret, safe=False)


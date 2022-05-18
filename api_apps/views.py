from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import ReCompact.dbm.DbObjects
import ReCompact.db_context
import api_models.ModelApps
from django.http import JsonResponse
import ReCompact.auth as rpt_auth
import api_apps.app_params
import ReCompact.api_input


# Create your views here.
@ReCompact.api_input.map_param(api_apps.app_params.AppParam)  # map request body to data view must have data
@require_http_methods(["POST"])
@rpt_auth.validator()
def create_app(request, data: api_apps.app_params.AppParam, error: ReCompact.api_input.Error):
    """
    Thêm mới hoặc cập nhật thông tin của application
    :param request:
    :param data:
    :param error:
    :return:
    """
    if error: return error.to_json()
    db = ReCompact.db_context.get_db()
    app = ReCompact.dbm.DbObjects.find_to_object(
        db,  # Căn cứ vào database
        api_models.ModelApps.sys_applications,  # Với model
        ReCompact.dbm.FILTER.Name == data.Name  # Tìm app thep tên
    )
    if app is None:
        error = ReCompact.api_input.Error()
        import re
        pat = re.compile(r"[A-Za-z][A-Za-z0-9\-]+")
        if not re.fullmatch(pat, data.Name):
            error.raise_invalid_field("Name")
            return error.to_json()
        if data.Domain.lower()!="localhost":
            pat = re.compile(r"/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/")
            if not re.fullmatch(pat, data.Domain):
                error.raise_invalid_field("Domain")
                return error.to_json()

    ReCompact.dbm.DbObjects.update(
        db,
        api_models.ModelApps.sys_applications,
        ReCompact.dbm.FILTER.Name == data.Name,
        ReCompact.dbm.SET(
            ReCompact.dbm.FIELDS.LoginUrl == data.LoginUrl,
            ReCompact.dbm.FIELDS.ReturnUrlAfterSignIn == data.ReturnUrlAfterSignIn
        )
    )

    pass


my_post = "POST"


@require_http_methods([my_post])
@rpt_auth.validator()
def list_apps(request, app_name):
    if app_name == 'admin' and request.current_user:
        import ReCompact.db_context
        db = ReCompact.db_context.get_db()

        agg = ReCompact.dbm.DbObjects.aggregrate(db, api_models.ModelApps.sys_applications)
        agg = agg.sort(
            ReCompact.dbm.DbObjects.FIELDS.Name.asc(),
            ReCompact.dbm.DbObjects.FIELDS.Domain.asc(),
        )

        return JsonResponse(list(agg), safe=False)


@require_http_methods(["POST"])
@rpt_auth.validator()
def get_app(request, app_name):
    db_app_name = request.data_body['AppName']
    import ReCompact.db_context
    import ReCompact.dbm
    db = ReCompact.db_context.get_db()
    ret = ReCompact.dbm.DbObjects.find_one_to_dict(
        db,
        api_models.ModelApps.sys_applications,
        ReCompact.dbm.FILTER.Name == db_app_name
    )
    return JsonResponse(ret, safe=False)

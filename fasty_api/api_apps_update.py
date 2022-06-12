import fasty
from fastapi import Depends, Body
import fasty.JWT
from .models import EditAppResutl,Error,ErrorType,AppInfo
import fasty.JWT
from fastapi import Response
import api_models.documents as docs

from ReCompact.db_async import get_db_context
@fasty.api_post("/{app_name}/apps/update/{app_edit}",response_model=EditAppResutl)
async def application_update(app_name: str, app_edit: str,Data: AppInfo = Body(embed=True) ,token: str = Depends(fasty.JWT.oauth2_scheme)):
    db_name =await fasty.JWT.get_db_name_async(app_name)
    if app_name!="admin":
        return Response(status_code=403)
    db_context = get_db_context(db_name)
    app = await db_context.find_one_async(docs.Apps,docs.Apps.Name==app_edit.lower())
    if app is None:
        ret= EditAppResutl(
            Data=None,
            Error = Error(
                Code =ErrorType.DATA_NOT_FOUND.value,
                Message="App was not found",
                Fields=[]
            )
        )
        return ret
    app = await db_context.update_one_async(
        docs.Apps,
        docs.Apps.Name==app_edit.lower(),
        docs.Apps.Decription==Data.Description
    )


    return None

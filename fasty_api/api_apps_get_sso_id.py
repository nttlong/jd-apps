import datetime
import uuid

from fastapi import Depends, status, Response
from fasty.JWT import get_oauth2_scheme
import uuid
import fasty.JWT
import fasty.JWT_Docs
from ReCompact.db_async import get_db_context
import api_models.documents as docs

@fasty.api_post("/{app_name}/sso")
async def do_sign_in(app_name: str, token: str = Depends(get_oauth2_scheme())):
    db_name = await fasty.JWT.get_db_name_async(app_name)
    if db_name is None:
        return Response(status_code=403)
    db_context = get_db_context(db_name)
    ret_id = str(uuid.uuid4())
    ret_url=fasty.config.app.root_url
    if app_name!='admin':
        app_item = await db_context.find_one_async(
            docs.Apps,
            docs.Apps.NameLower==app_name.lower()
        )
        ret_url = app_item[docs.Apps.ReturnUrlAfterSignIn.__name__]
    ret = await db_context.insert_one_async(
        fasty.JWT_Docs.SSOs,
        fasty.JWT_Docs.SSOs.Token == token,
        fasty.JWT_Docs.SSOs.SSOID == ret_id,
        fasty.JWT_Docs.SSOs.CreatedOn==datetime.datetime.utcnow(),
        fasty.JWT_Docs.SSOs.ReturnUrlAfterSignIn==ret_url
    )

    return {"token": ret_id}

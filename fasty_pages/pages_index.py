import fasty
from fastapi import FastAPI, Request,Response
import os
@fasty.page_get("/")
async def page_index(request: Request):
    app_data =dict(
        full_url_app=fasty.config.app.root_url,
        full_url_root=fasty.config.app.root_url,
        api_url=fasty.config.app.api_url
    )
    return fasty.config.app.templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "app": app_data
        }
    )
@fasty.page_get("/{directory:path}")
async def page_single(directory:str, request: Request):
    check_dir_path = os.path.join(fasty.config.app.static, directory.replace('/', os.sep))
    if not os.path.exists(check_dir_path):
        return Response(status_code=401)
    app_data =dict(
        full_url_app=fasty.config.app.root_url,
        full_url_root=fasty.config.app.root_url,
        api_url=fasty.config.app.api_url
    )
    return fasty.config.app.templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "app": app_data
        }
    )
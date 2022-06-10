import fasty
from fastapi import FastAPI, Request

@fasty.page_get("/")
async def read_item(request: Request):
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
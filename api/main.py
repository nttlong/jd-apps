import os
import sys
import pathlib
import fasty
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
"""
Nạp môi trường 
"""
# from fastapi import FastAPI
#
# app = FastAPI()

app = fasty.install_fastapi_app(__name__)
import fasty_api
@fasty.api_get('/xyz')
async def root():
    return {"message": "Hello World"}
print(__name__)

#uvicorn api.main:app --reload
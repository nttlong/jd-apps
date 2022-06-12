"""
API liệt kê danh sách các file
"""
import ReCompact.dbm
import fasty
from fastapi import FastAPI, Request
import api_models.documents as docs
from ReCompact import db_async
import json
from db_connection import connection, default_db_name
from . import api_files_schema
from datetime import datetime, timedelta
from typing import Union
import fasty.JWT
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

@fasty.api_post("/accounts/token",response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    app_name=""
    if '/' in form_data.username:
        items =form_data.username.split('/')
        app_name =items[0]
        username =form_data.username[app_name.__len__()+1:]
    elif '@' in form_data.username:
        items = form_data.username.split('@')
        app_name = items[-1]
        username = form_data.username[0:-app_name.__len__()-1]

    user =await fasty.JWT.authenticate_user_async(app_name, username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=fasty.config.app.jwt.access_token_expire_minutes)
    access_token =fasty.JWT. create_access_token(
        data={
            "sub": user[fasty.JWT.JWT_Docs.Users.Username.__name__] ,
            "application":app_name
        },
        expires_delta=access_token_expires

    )
    return {"access_token": access_token, "token_type": "bearer"}
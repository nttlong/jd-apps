from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import fasty
import fasty.JWT
class TokenData(BaseModel):
    username: Union[str, None] = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/accounts/token")

async def do_get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, fasty.config.app.jwt.secret_key, algorithms=[fasty.config.app.jwt.algorithm])
        username: str = payload.get("sub")
        app_name =payload.get("application")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user =await fasty.JWT.get_user_by_username_async(app_name, token_data.username)
    if user is None:
        raise credentials_exception
    return dict(
        UserId=user["_id"],
        UserName=user[fasty.JWT.JWT_Docs.Users.Username.__name__],
        Email=user[fasty.JWT.JWT_Docs.Users.Email.__name__],
        Application=app_name
    )
@fasty.api_post("/accounts/user")
async def post_current_user(token: str = Depends(oauth2_scheme)):
    return await do_get_current_user( token)
@fasty.api_get("/accounts/user")
async def get_current_user(token: str= Depends(oauth2_scheme) ):
    return await do_get_current_user(token)
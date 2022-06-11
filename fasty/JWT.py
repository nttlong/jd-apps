"""
Quản lý JWT
"""
import bson
import motor.motor_asyncio
from . import JWT_Docs
from datetime import datetime, timedelta
from typing import Union
import asyncio
import ReCompact.db_async
import motor
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
USER_COLLECTION_NAME ="sys_jwt_users"
CONNECTION_STRING= None
def set_connection_string(cnn:str):
    global CONNECTION_STRING
    CONNECTION_STRING =cnn
    ReCompact.db_async.set_connection_string(cnn)
def check():
    global CONNECTION_STRING
    if CONNECTION_STRING is None:
        raise Exception("Please call 'fasty.JWT.set_connection_string'")
def sync(*args, **kwargs):
    """
    Khử sync
    :param args:
    :param kwargs:
    :return:
    """
    loop = asyncio.get_event_loop()
    coroutine = args[0]
    ret = loop.run_until_complete(coroutine)
    return ret
async def get_user_by_username_async(db_name:str,username:str):
    check()
    dbcntx= ReCompact.db_async.get_db_context(db_name)
    user= await dbcntx.find_one_async(JWT_Docs.Users,JWT_Docs.Users.UsernameLowerCase==username.lower())
    return user
def get_user_by_username(db_name:str,username:str):
    return sync(get_user_by_username_async(db_name,username))

async def get_user_by_user_id_async(db_name:str,user_id:str):
    check()
    dbcntx= ReCompact.db_async.get_db_context(db_name)
    user= await dbcntx.find_one_async(JWT_Docs.Users,JWT_Docs.Users._id==bson.ObjectId(user_id))
    return user
def get_user_by_user_id(db_name:str,username:str):
    return sync(get_user_by_user_id_async(db_name,username))

async def create_user_async(db_name:str,Username:str,Password:str,Email:str):
    check()
    dbcntx = ReCompact.db_async.get_db_context(db_name)

    UsernameLower =Username.lower()
    HashPassword= get_password_hash(UsernameLower+"/"+Password)
    try:
        ret_user = await dbcntx.insert_one_async(
            JWT_Docs.Users,
            JWT_Docs.Users.Username==Username,
            JWT_Docs.Users.UsernameLowerCase==UsernameLower,
            JWT_Docs.Users.Email==Email,
            JWT_Docs.Users.HashPassword==HashPassword,
            JWT_Docs.Users.IsLocked==False,
            JWT_Docs.Users.CreatedOnUTC==datetime.now(),
            JWT_Docs.Users.CreatedOn == datetime.utcnow()
        )
    except ReCompact.db_async.Error as e:
        if e.code==ReCompact.db_async.ErrorType.DUPLICATE_DATA:
            if (set([
                JWT_Docs.Users.Username.__name__,
                JWT_Docs.Users.UsernameLowerCase.__name__]) & set(e.fields)).__len__()>0:
                e.message="User is already"
            if (set([
                JWT_Docs.Users.Email.__name__]) & set(e.fields)).__len__()>0:
                e.message="Email is already"
        raise e
def create_user(db_name:str,Username:str,Password:str,Email:str):
    return sync(create_user_async(db_name,Username,Password,Email))



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def verify_password(plain_password, hashed_password):
    global pwd_context
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_async(app_name:str, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get(JWT_Docs.Users.Username.__name__)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username_async(app_name,token_data.username)
    user["Id"]=user["_id"]
    user["username"]=user[JWT_Docs.Users.UsernameLowerCase.__name__]
    if user is None:
        raise credentials_exception
    return dict(
        UserId=user["Id"],
        Username=user["UserName"],
        Email =user["Email"]
    )
def get_current_user(app_name:str,token: str = Depends(oauth2_scheme)):
    import asyncio
    loop = asyncio.get_event_loop()
    coroutine = get_current_user_async(app_name,token)
    ret = loop.run_until_complete(coroutine)
    return ret
async def get_current_active_user_async(current_user = Depends(get_current_user_async)):
    if current_user.get(JWT_Docs.Users.IsLocked.__name__):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
async def authenticate_user_async(app_name, username: str, password: str):
    user = await get_user_by_username_async(app_name,username)
    if not user:
        return False
    if not verify_password(username.lower()+"/"+ password, user[JWT_Docs.Users.HashPassword.__name__]):
        return False
    return user
def authenticate_user(app_name, username: str, password: str):
    return sync(authenticate_user_async(app_name,username,password))

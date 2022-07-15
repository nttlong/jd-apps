import datetime
import uuid

from fastapi import Request, Response
from ReCompact.db_context import get_db, get_db_connection
from ReCompact import db_async
from jose import JWTError, jwt
import fasty
import jose
from fastapi.security.utils import get_authorization_scheme_param
import fasty.JWT
import threading
from .share_key_models import share_key_docs
from enum import Enum


class AccessExpireEnum(Enum):
    """
    Enum of Life time of Access key
    """
    DEFAUTL = 0
    """
    life time of Access key is life time of token 
    """
    FOREVER = 1
    """
    Never expire
    """
    ONE_TIME = 2
    """
    Expire immediately after use
    """
    PRIVATE = 3
    """
    Serve for current user
    """

__cache_access_key__ = {}
__cache_access_key_reverse__ = {}
__lock__ = threading.Lock()


class ShareKeyInfo:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Context:
    def __init__(self):
        self.request: Request
        self.token: str = None
        self.username: str = None
        self.application_name = None
        """
        The application name get from tokn
        """
        self.access_application_name = None
        """
        The application get from url
        """
        self.is_forbidden = False

    def get_forbidden_response(self):
        return Response(status_code=403)

    async def get_db_context(self) -> db_async.DbContext:
        db_name = await fasty.JWT.get_db_name_async(self.application_name)
        return db_async.get_db_context(db_name)

    def __gen_key__(self,expire: AccessExpireEnum, key: str, url_path: str):
        if expire.PRIVATE:
            return f"{url_path}/{key}/{self.application_name}/{self.username}"
        return f"{url_path}/{key}/{self.application_name}"

    async def get_share_key_info(self, share_key: str):
        global __lock__
        global __cache_access_key__
        global __cache_access_key_reverse__
        ret = __cache_access_key_reverse__.get(share_key)
        if ret is None:
            db = await self.get_db_context()
            db_item = await  db.find_one_async(
                share_key_docs,
                share_key_docs.ShareKey == share_key
            )
            if db_item is None:
                return None
            else:
                __lock__.acquire()
                __cache_access_key__[db_item.get(share_key_docs.Key.__name__)] = share_key
                __cache_access_key_reverse__[share_key] = dict(
                    url=db_item.get(share_key_docs.Url.__name__),
                    created_by=db_item.get(share_key_docs.CreateBy.__name__),
                    app_name=db_item.get(share_key_docs.AppName.__name__),
                    share_key=share_key,
                    _id=share_key,
                    created_on=db_item.get(share_key_docs.CreatedOnUTC.__name__),
                    expire_type=db_item.get(share_key_docs.ExpireType.__name__)
                )
                __lock__.release()

        ret = __cache_access_key_reverse__.get(share_key)
        if self.request.scope.get('route').path == ret.get('url'):
            return ret
        return None

    async def create_share_key(self, access_key: str, expire: AccessExpireEnum, end_point_func)->ShareKeyInfo:
        """
        Create sso id for an endpoint.
        That mean with sso id user can only access to api end_point_func
        end_point_func is a function has been added to route
        example:
            @fastapi.get('api/a/')
            async def function_a(context=Depends(Context()):
                if context.get_share_key_info():
                #check does sso id accept?
                ...
            @fasapi.post('api/b/')
            async def function_b(context=Depends(Context()):
                access_key = context.create_share_key(function_a)

        :param expire:
        :param end_point_func:
        :param access_key:

        :return:
        """
        """
        fastapi.routing.APIRoute
        self.request.app.routes
        name,path
        """
        global __lock__
        global __cache_access_key__
        global __cache_access_key_reverse__

        if not callable(end_point_func):
            raise Exception("sso id accept function endpoint")
        end_point_url_path = None
        for x in self.request.app.routes:
            if x.name == end_point_func.__name__:
                end_point_url_path = x.path
                break
        if end_point_url_path is None:
            raise Exception(f"{end_point_func.__name__} in {end_point_func.__module__} must be an API\n"
                            f"Please, preview {end_point_func.__code__}")
        key = self.__gen_key__(expire, access_key, end_point_url_path)

        if __cache_access_key__.get(key) is None:
            __lock__.acquire()
            try:
                db = await self.get_db_context()
                db_item = await db.find_one_async(
                    share_key_docs,
                    share_key_docs.Key == key
                )
                if db_item is None:
                    share_key = str(uuid.uuid4())
                    share_key_data = dict(
                        url=end_point_url_path,
                        created_by=self.username,
                        app_name=self.application_name,
                        share_key=share_key,
                        _id=share_key,
                        created_on=datetime.datetime.utcnow(),
                        expire_type=expire.name
                    )
                    __cache_access_key__[key] = share_key
                    __cache_access_key_reverse__[share_key] = share_key_data

                    def sync_to_db():
                        db.insert_one(
                            share_key_docs,
                            share_key_docs.ShareKey == share_key,
                            share_key_docs.AppName == self.application_name,
                            share_key_docs.CreateBy == self.username,
                            share_key_docs._id == share_key,
                            share_key_docs.Url == end_point_url_path,
                            share_key_docs.Key == key,
                            share_key_docs.CreatedOnUTC == share_key_data['created_on'],
                            share_key_docs.ExpireType == share_key_data['expire_type']
                        )

                    th_sync = threading.Thread(target=sync_to_db, args=())
                    th_sync.start()
                else:
                    __cache_access_key__[key] = db_item.get(share_key_docs.ShareKey.__name__)
                    __cache_access_key_reverse__[__cache_access_key__[key]] = dict(
                        url=db_item.get(share_key_docs.Url.__name__),
                        created_by=db_item.get(share_key_docs.CreateBy.__name__),
                        app_name=db_item.get(share_key_docs.AppName.__name__),
                        share_key=__cache_access_key__[key],
                        _id=__cache_access_key__[key],
                        created_on=db_item.get(share_key_docs.CreatedOnUTC.__name__),
                        expire_type=db_item.get(share_key_docs.ExpireType.__name__)
                    )

            finally:
                __lock__.release()
        return ShareKeyInfo(access_key, __cache_access_key__.get(key))

    async def get_token(self, request: Request):
        token = request.cookies.get('access_token_cookie', None)
        if token is None:
            authorization: str = request.headers.get("Authorization")
            if authorization is not None:
                scheme, token = get_authorization_scheme_param(authorization)
        if token is None:
            cors_token = request.query_params.get('token', None)
            if cors_token is not None:
                token = await self.get_token_by_sso_id(cors_token)
        if token is not None:
            try:
                ret_data = jwt.decode(token, fasty.config.app.jwt.secret_key,
                                      algorithms=[fasty.config.app.jwt.algorithm],
                                      options={"verify_signature": False},
                                      )
                self.username = ret_data.get("sub")
                self.application_name = ret_data.get("application")
                if request.scope.get('path_params') is not None:
                    self.access_application_name = request.scope.get('path_params').get('app_name')
                    self.is_forbidden = True

            finally:
                self.token = token
                self.access_application_name = self.access_application_name = request.scope.get('path_params').get(
                    'app_name')
                if self.access_application_name is not None:
                    db_name = await fasty.JWT.get_db_name_async(self.access_application_name)
                    if db_name is not None:
                        self.application_name = self.access_application_name
                    else:
                        self.is_forbidden = True
                return token
        else:
            self.access_application_name= self.access_application_name = request.scope.get('path_params').get('app_name')
            if self.access_application_name is not None:
                db_name = await fasty.JWT.get_db_name_async(self.access_application_name)
                if db_name is not None:
                    self.application_name= self.access_application_name
                else:
                    self.is_forbidden = True
        return token

    async def __call__(self, request: Request):
        self.request = request
        self.token = await self.get_token(self.request)
        return self

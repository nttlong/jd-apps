import datetime

import bson

import ReCompact
import ReCompact.db_async
@ReCompact.document(
    name="Sys_JWT_Users",
    keys=["Email","Username","UsernameLowerCase"],
    indexes=["HashPassword"]
)
class User:
    _id = (bson.ObjectId)
    Username =(str)
    UsernameLowerCase =(str)
    HashPassword=(str)
    Email=(str)
    IsLocked =(bool),
    CreatedOn=(datetime.datetime)
    CreatedOnUTC = (datetime.datetime)
    ModifiedOn =(datetime.datetime)
    IsSysAdmin=(bool)

Users = User()
"""
Mongodb document of user
"""
import datetime

from ReCompact import document
@document(
    name="SYS_PER_ShareKeys",
    indexes=["AppName","Key"]

)
class ShareKey:
    _id = (str)
    ShareKey = (str)
    AppName = (str)
    CreateBy =(str)
    Url = (str)
    Key = (str)
    CreatedOnUTC =(datetime.datetime)
    ExpireType = (str)


share_key_docs =ShareKey()
"""
Model share key
"""

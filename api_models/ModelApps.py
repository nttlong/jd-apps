import ReCompact.dbm
import datetime
@ReCompact.dbm.table(
    "sys_applications"

)
class sys_applications:
    import bson
    _id = ReCompact.dbm.field(data_type=str)
    Name = ReCompact.dbm.field(data_type=str, is_require=True)
    """
    Ten cua app
    """
    RegisteredBy = ReCompact.dbm.field(data_type=str,is_require=True)
    RegisteredOn = ReCompact.dbm.field(data_type=datetime.datetime, is_require=True)
    Domain = ReCompact.dbm.field(data_type=str, is_require=True)
    UrlLogin = ReCompact.dbm.field(data_type=str, is_require=True)
    ReturnUrlAfterSigin = ReCompact.dbm.field(data_type=str, is_require=True)
    SercrectKey = ReCompact.dbm.field(data_type=str)



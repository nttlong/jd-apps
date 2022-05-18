import ReCompact.dbm
import datetime
@ReCompact.dbm.table(
    "DocUploadRegister"

)
class DocUploadRegister:
    import bson
    _id = ReCompact.dbm.field(data_type=str)
    FileName = ReCompact.dbm.field(data_type=str, is_require=True)
    """
    Ten cua app
    """
    RegisteredOn = ReCompact.dbm.field(data_type=datetime.datetime, is_require=True)


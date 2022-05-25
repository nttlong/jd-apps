import ReCompact.dbm
import datetime


@ReCompact.dbm.table(
    "DocUploadRegister",
    keys=["ServerFileName", "FullFileName"],
    index=[
        "RegisteredOn",
        "Status",
        "FileExt",
        "FileName",
        "MainFileId",
        "ThumbFileId",
        "OriginalFileId"
    ]

)
class DocUploadRegister:
    import bson
    _id = ReCompact.dbm.field(data_type=str)
    FileName = ReCompact.dbm.field(data_type=str, is_require=True)
    """
    Ten cua app
    """
    RegisterOn = ReCompact.dbm.field(data_type=datetime.datetime, is_require=True)
    LastModifiedOn = ReCompact.dbm.field(data_type=datetime.datetime, is_require=False)
    Status = ReCompact.dbm.field(data_type=int, is_require=True)
    SizeInBytes = ReCompact.dbm.field(data_type=int, is_require=True)
    ChunkSizeInKB = ReCompact.dbm.field(data_type=int, is_require=True)
    ChunkSizeInBytes = ReCompact.dbm.field(data_type=int, is_require=True)
    NumOfChunks = ReCompact.dbm.field(data_type=int, is_require=True)
    FileExt = ReCompact.dbm.field(data_type=str, is_require=False)
    SizeInHumanReadable = ReCompact.dbm.field(data_type=str, is_require=False)
    PercentageOfUploaded = ReCompact.dbm.field(data_type=float, is_require=False)
    ServerFileName = ReCompact.dbm.field(data_type=str, is_require=False)
    RegisteredBy = ReCompact.dbm.field(data_type=str, is_require=False)
    IsPublic = ReCompact.dbm.field(data_type=bool, is_require=True)
    FullFileName = ReCompact.dbm.field(data_type=str, is_require=True)
    ThumbWidth = ReCompact.dbm.field(data_type=int, is_require=False)
    ThumbHeight = ReCompact.dbm.field(data_type=int, is_require=False)
    MimeType = ReCompact.dbm.field(data_type=str, is_require=False)
    SizeUploaded =ReCompact.dbm.field(data_type=int,is_require=False)
    NumOfChunksCompleted = ReCompact.dbm.field(data_type=int, is_require=False)
    MainFileId = ReCompact.dbm.field(data_type=bson.ObjectId)
    ThumbFileId = ReCompact.dbm.field(data_type=bson.ObjectId)
    ThumbId  = ReCompact.dbm.field(data_type=str) # depreciate after jun 2022
    HasThumb = ReCompact.dbm.field(data_type=bool)
    OriginalFileId = ReCompact.dbm.field(data_type=bson.ObjectId) # Trường hợp xử lý OCR thành công
    # thông tin này sẽ lưu lại file gốc, trong khi đó file gốc sẽ được cập nhật lại bằng nôi dung file mới
    # đã được OCR




    @property
    def id(self):
        return self._id

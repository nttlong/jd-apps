import quicky.object_contraints
@quicky.object_contraints.contraints()
class FileUplaodInfo:
    FileName=(str,True)
    FileSize=(int,True)


data = FileUplaodInfo({
    FileUplaodInfo.FileName : "123",
    FileUplaodInfo.FileSize : None
})
err=data.get_error()
if err:
    print(err.to_dict())
else:
    print(data.FileSize)
    data.FileSize=None
    print("OK")
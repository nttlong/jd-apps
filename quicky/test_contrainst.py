import quicky.object_contraints
@quicky.object_contraints.contraints()
class FileUplaodInfo:
    FileName=(str,True)
    FileSize=(int,True)



data = FileUplaodInfo({
    FileUplaodInfo.FileName : "123",
    FileUplaodInfo.FileSize : 123
})
err=data.get_error()
if err:
    print(err.to_dict())
else:
    print(data.FileSize)
    data.FileSize=123456
    print("OK")
    data.to_dict()
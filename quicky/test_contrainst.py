import quicky.object_contraints
@quicky.object_contraints.contraints()
class FileUplaodInfo:
    FileName=(str,True)
    FileSize=(int,True)


data = FileUplaodInfo(dict(x=1))
err=data.get_error()
if err:
    print(err.to_dict())
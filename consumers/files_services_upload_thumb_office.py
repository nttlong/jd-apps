"""
var UserProfileId = Guid.NewGuid().ToString();
            var UserProfileFullPath = Path.Combine(ProfileDir, UserProfileId);
            Directory.CreateDirectory(UserProfileFullPath);


            var uno =string.Format("uno:socket,host={0},port={1};urp;Negotiate=0,ForceSynchronous=0;",UnonHost,UnoPort.ToString("0000"));
            if (!File.Exists(sofficePath))
                throw new Exception("'" + sofficePath + "' was not found");
            if (!File.Exists(officeFile))
                throw new Exception("'" + officeFile + "' was not found");
            var direcrory = new FileInfo(officeFile).Directory.FullName;

            return await Task.Run<string>(() =>
            {

                var thumbnai = officeFile.Split("\\").ToList();
                var namedist = thumbnai[thumbnai.Count() - 1];
                ProcessStartInfo info;


                try
                {
                    using (var th = new Process())
                    {

                        info = th.StartInfo;

                        info.FileName = sofficePath;
                        var arg = "--outdir {0} {1}";
                        var argList = new List<string>();
                        argList.Add("--headless");
                        argList.Add("--convert-to png");
                        argList.Add(string.Format(@"--accept={0}", uno));



                        argList.Add(@"-env:UserInstallation=file:///"+UserProfileFullPath.Replace(@"\", @"/"));
                        arg = string.Format(arg, tmpDir, officeFile, uno);

                        argList.Add(arg);
                        info.Arguments = string.Join(" ", argList);

                        info.UseShellExecute = true;
                        info.CreateNoWindow = false;
                        if (!string.IsNullOrEmpty(Username))
                        {
                            info.UserName = Username;
                            info.PasswordInClearText = Password;
                            info.Domain = domain;
                        }

                        th.EnableRaisingEvents = true;
                        th.OutputDataReceived += (S,E)=> {
                            Console.WriteLine($"----------------------------------------------");
                            Console.WriteLine($"Process file '{officeFile}' recive data at :" + DateTime.Now.ToString("dd-MM-yyyy hh:mm;ss"));
                            Console.WriteLine($"----------------------------------------------");
                        };
                        th.ErrorDataReceived += (S, E) =>
                        {
                            Console.WriteLine($"----------------------------------------------");
                            Console.WriteLine($"'{sofficePath}' is error :");
                            Console.WriteLine(E.Data);
                            Console.WriteLine($"----------------------------------------------");
                        };
                        th.Exited += (S, E) =>
                        {
                            Console.WriteLine($"----------------------------------------------");
                            Console.WriteLine($"'{sofficePath}'");
                            Console.WriteLine("Exist at :" + DateTime.Now.ToString("dd - MM - yyyy hh: mm:ss"));
                            Console.WriteLine($"----------------------------------------------");

                        };

                        th.Start();
                        th.WaitForExit();
                        return Path.Combine(tmpDir,  Path.GetFileNameWithoutExtension(new FileInfo(officeFile).Name)+".png");


                    }
                }
                catch (Exception)
                {

                    throw;
                }




            });


"""
import config
import ReCompact_Kafka.consumer


import logging


def handler_use_aspose(consumer: ReCompact_Kafka.consumer.Consumer_obj, msg, logger: logging.Logger):
    """
    S??? d???ng aspose c???n ph???i c?? b???n quy???n ch???y nhanh h??n
    :param consumer:
    :param msg:
    :param logger:
    :return:
    """
    import config
    import os
    import uuid
    import aspose.words as aw

    data = consumer.get_json(msg)

    file_path = data["FilePath"]  # ???????ng d???n ?????n file v???t l??
    logger.info(f"Create Office Thumb file {file_path}")
    logger.info(data)
    upload_info = data["UploadInfo"]  # Th??ng tin l??c upload
    if upload_info["FileExt"] == "pdf":
        consumer.commit(msg)
        return
    app_name = data["AppName"]  # T??n App
    ThumbWidth, ThumbHeight = upload_info.get('ThumbWidth', 700), upload_info.get('ThumbHeight', 700)
    out_put_dir = os.path.join(config.temp_thumbs, app_name)
    if not os.path.isdir(out_put_dir):
        os.mkdir(out_put_dir)
    out_put_file = os.path.join(out_put_dir, f"{upload_info['_id']}.png")
    # load document
    doc = aw.Document(file_path)

    # set output image format
    options = aw.saving.ImageSaveOptions(aw.SaveFormat.PNG)

    # loop through pages and convert them to PNG images
    for pageNumber in range(doc.page_count):
        options.page_set = aw.saving.PageSet(pageNumber)
        doc.save(out_put_file, options)
        break

    uno = "uno:socket,host=localhost,port=10;urp;Negotiate=0,ForceSynchronous=0;"


def handler_use_libre_office(consumer: ReCompact_Kafka.consumer.Consumer_obj, msg, logger: logging.Logger):
    """
    S??? d???ng Libre Office
    Ch?? ??: Kh??ng c???n b???t l???i trong tr?????ng h???p kh??ng c???n thi???t
           N???u l???i x??y ra h??? th???ng s??? t??? ?????ng ghi nh???n
    :param consumer:
    :param msg:
    :param logger:
    :return:
    """
    import subprocess
    import uuid
    import config
    import os
    import time
    data = consumer.get_json(msg)
    file_path = data["FilePath"]  # ???????ng d???n ?????n file v???t l??
    upload_info = data["UploadInfo"]
    file_ext = upload_info["FileExt"]
    file_name = upload_info["FileName"]
    if file_ext=="pdf":
        """
        file pdf b??? qua
        """
        consumer.commit(msg)
        return
    logger.info(f"Create Office Thumb file {file_path}")
    logger.info(data)
    app_name = data["AppName"]
    upload_info = data["UploadInfo"]  # Th??ng tin l??c upload
    upload_id = upload_info["_id"]
    image_file_path = os.path.join(config.temp_thumbs, app_name, f"{upload_id}.png")
    out_put_dir = os.path.join(config.temp_thumbs, app_name)
    if not os.path.isfile(image_file_path):
        user_profile_id = str(uuid.uuid4())  # T???o user profile gi???, n???u kg c?? ??i???u n??y LibreOffice ch??? t???o 1 instance,
        # kg x??? l?? song song ???????c
        full_user_profile_path = os.path.join(config.temp_libre_office_user_profile_dir, user_profile_id)
        uno = f"Negotiate=0,ForceSynchronous=1;"

        if not os.path.isdir(out_put_dir):
            os.makedirs(out_put_dir)
        if not os.path.isfile(file_path):
            print(file_path)
            return
        arg = f"--outdir { out_put_dir} {file_path.replace(os.sep,'/')}"
        arg_list = [
            f'"{config.libre_office_path}"',

            "--headless",
            "--convert-to png",
            f"--accept={uno}",
            f"-env:UserInstallation=file:///{full_user_profile_path.replace(os.sep, '/')}",
            arg
        ]
        full_comand_line = " ".join(arg_list)
        logger.info(full_comand_line)
        # full_comand_line = f'"{config.libre_office_path}"  --convert-to png --outdir {out_put_dir} -env:UserInstallation=file:///{full_user_profile_path.replace(os.sep, "/")} '
        logger.debug(full_comand_line)
        # full_comand_line =r'"C:\Program Files\LibreOffice\program\soffice.exe"  --convert-to png --outdir C:\test C:\test\x.docx -env:UserInstallation=file:///C:/dj-apps-2022-05-25/jd-apps/consumers/LibreOfficeTempProfiles/xxx --headless --accept=Negotiate=0,ForceSynchronous=1;'
        p = subprocess.Popen(full_comand_line  , shell=False)


        ret=p.communicate() # ?????i
        import shutil
        shutil.rmtree(full_user_profile_path)
        logger.info(f"Process file {file_path} to image is finish")
    thumb_file_path = os.path.join(out_put_dir, f"{upload_id}_thumb.png")
    if not os.path.isfile(thumb_file_path):
        ThumbWidth, ThumbHeight = upload_info.get('ThumbWidth', 700), upload_info.get('ThumbHeight', 700)
        """
        D??ng tren lay k??ch th????c cua thumb
        Anh thum thuc su se co lai vua van voi khung
    
        """

        from PIL import Image


        img = Image.open(image_file_path)
        w, h = img.size
        rate = ThumbWidth / w  # M???c d???nh b??p theo b??? r???ng
        if h > w:  # Nh??ng v?? b??? d???c l???n h??n b??? r???ng
            rate = ThumbHeight / h  # n??n b??p theo b??? d???c
        nh = int((float(h) * float(rate)))
        nw = int((float(w) * float(rate)))
        img = img.resize((nw, nh), Image.ANTIALIAS)
        img.save(thumb_file_path)
        logger.info(f"Create thumb {file_path} is success at {thumb_file_path}")
    """
    B?????c cu???i c??ng c???p nh???t ???nh thumb
    """

    import ReCompact.dbm.DbObjects # D??ng ????? thao t??c d??? li???u ter6n mongodb
    import mongo_db # D??ng ????? l???y database thao t??c
    import ReCompact.db_context # D??ng ????? t???o file tr??n mongodb
    import api_models.Model_Files # S??? d???ng model
    import ReCompact.dbm
    db = mongo_db.get_db(app_name)
    """
    ????a file thumb v??o fs.file c???a  database
    """
    fs = ReCompact.db_context.create_mongodb_fs_from_file(
        db=db,
        full_path_to_file= thumb_file_path
    )
    logger.info(f"save {thumb_file_path} is success at ")
    """
    ???? ????a file v??o xong
    """

    ret =ReCompact.dbm.DbObjects.update(
        db,
        data_item_type= api_models.Model_Files.DocUploadRegister,
        filter= ReCompact.dbm.FILTER._id == upload_id,
        updator= ReCompact.dbm.SET (
            ReCompact.dbm.FIELDS.ThumbFileId==fs._id,
            ReCompact.dbm.FIELDS.HasThumb==True
        )
    )
    logger.info(f"update thumb id of {upload_id} with value  {thumb_file_path}")
    print(f"update thumb id of {file_name} with value  {thumb_file_path}")
    consumer.commit(msg)
    logger.info(f"Create Office Thumb file {file_path} is Finish")
    logger.info(data)
def error(err,msg,logger):
    logger.debug(err)
def error1(err,msg,logger):
    logger.debug(err)

import uuid
__id__ =str(uuid.uuid4())
import ReCompact_Kafka.consumer

consumer = ReCompact_Kafka.consumer.create(
    topic_id="files.services.upload.thumb.office",
    group_id=f"files.services.upload.thumb.office.{__id__}",
    server =config.kafka_broker,
    on_consum= handler_use_libre_office,
    on_consum_error=error,
)
if __name__ == "__main__":
    consumer.run()
#C:\dj-apps-2022-05-25\jd-apps\venv\Scripts\python.exe C:\dj-apps-2022-05-25\jd-apps\consumers\files_services_upload_thumb_office.py
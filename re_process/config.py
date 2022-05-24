kafka_broker = ["192.168.18.36:9092"]
office_extension = ";docx;doc;xls;xlsx;txt;pdf;ppx;pptx;json;psd;html;xml;js;otg;svg;vsd;" \
    .split(';');
office_extension += ".ODT;.CSV;.DB;.DOC;.DOCX;.DOTX;.FODP;.FODS;.FODT;.MML" \
                    ";.ODB;.ODF;.ODG;.ODM;.ODP;.ODS;.OTG;.OTP;.OTS;.OTT;.OXT" \
                    ";.PPTX;.PSW;.SDA;.SDC;.SDD;.SDP;.SDW;.SLK;.SMF;.STC" \
                    ";.STD;.STI;.STW;.SXC;.SXG;.SXI;.SXM;.UOF;.UOP;.UOS;.UOT" \
                    ";.VSD;.VSDX;.WDB;WPS;.WRI;.XLS;.XLSX".lower().split(';.')
temp_thumbs = r"\\192.168.18.36\Share\DjangoWeb\temp_thumb"  # Thư mục tạm để xử lý ảnh thumbs

poppler_path = r"C:\dj-apps\jd-apps\poppler-0.68.0\bin"
libre_office_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
temp_libre_office_user_profile_dir = r"C:\dj-apps-2022-05-25\jd-apps\LibreOfficeTempProfiles"

import os

if not os.path.isdir(temp_thumbs):
    raise Exception(f"'{temp_thumbs}' was not found")
# if  not os.path.isdir(poppler_path):
#     raise Exception(f"'{poppler_path}' was not found")
if not os.path.isfile(libre_office_path):
    raise Exception(f"'{libre_office_path}' was not found"
                    f"Thee need LibreOffice fo office file convert")
if not os.path.isdir(temp_libre_office_user_profile_dir):
    raise Exception(f"'{temp_libre_office_user_profile_dir}' was not found"
                    f"Need Temporary profile folder for Libre Office when it run in parallel")
mongo_db_config = dict(

    host=["192.168.18.36"],
    port=27018,
    username="admin-doc",
    password="123456",
    authSource="lv-docs",
    authMechanism="SCRAM-SHA-1",
    replicaSet="rs0"

)

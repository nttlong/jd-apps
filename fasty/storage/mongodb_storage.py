from fasty.storage.must_impl import MustImplement
from fasty.storage.base_storage import base_storage
from pymongo.mongo_client import MongoClient

from gridfs import GridFS
import os
import bson


@MustImplement()
class mongodb_storage(base_storage):
    """
    Provider file storage in mongodb GridFS
    """

    def __init__(self, config_dir: str, yaml_path, data: dict):
        self.config_data = data.get(self.get_key())
        if self.config_data is None:
            raise Exception(f"'{self.get_key()}' was not found in '{yaml_path}'")
        if not isinstance(self.config_data, dict):
            raise Exception(f"'{self.get_key()}' in '{yaml_path}' must have attributes")
        self.host = self.config_data.get('host')
        if self.host is None:
            raise Exception(f"'{self.get_key()}.host' was not found in '{yaml_path}'")
        self.port = self.config_data.get('port')
        if self.port is None:
            raise Exception(f"'{self.get_key()}.port' was not found in '{yaml_path}'")
        self.username = self.config_data.get('username')
        if self.username is None:
            raise Exception(f"'{self.get_key()}.username' was not found in '{yaml_path}'")
        self.password = self.config_data.get('password')
        if self.password is None:
            raise Exception(f"'{self.get_key()}.password' was not found in '{yaml_path}'")
        self.authSource = self.config_data.get('authSource')
        if self.authSource is None:
            raise Exception(f"'{self.get_key()}.authSource' was not found in '{yaml_path}'")
        self.replicaSet = self.config_data.get('replicaSet')
        if self.replicaSet is None:
            raise Exception(f"'{self.get_key()}.replicaSet' was not found in '{yaml_path}'\n"
                            f"if you would not like to use replicaSet, just set blank\n"
                            f"looks like these: replicaSet:''")
        self.authMechanism = self.config_data.get('authMechanism', None)
        if self.authMechanism is None:
            raise Exception(f"'{self.get_key()}.authMechanism' was not found in '{yaml_path}'")
        self.temp_dir = self.config_data.get('temp_dir')
        if self.temp_dir is None:
            raise Exception(f"'{self.get_key()}.temp_dir' was not found in '{yaml_path}'")
        if not os.path.isdir(self.temp_dir):
            raise Exception(f"'{self.temp_dir}' was not found")
        connect_config = {}
        for k, v in self.config_data.items():
            if v is not None and v != '':
                connect_config[k] = v
        if self.replicaSet == '':
            self.client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                authSource=self.authSource,
                authMechanism=self.authMechanism)

        else:
            self.client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                authSource=self.authSource,
                authMechanism=self.authMechanism,
                replicaSet=self.replicaSet
            )

    def get_key(self) -> str:
        return "mongodb"

    def get_root_directory(self) -> str:
        """
        Get temp directory when user upload file
        :return:
        """
        return self.temp_dir

    async def append_data(self, rel_path_to_directory: str, server_file_name_only: str, filename: str,
                          data: bytes) -> str:
        """
        Thêm nội dung vào file, nếu file chưa có tạo mới.

        Create or append data to file and return unique id of file
        With unique id of file we can get full content of file
        :param server_file_name_only: the name of file at server without extension
        :param rel_path_to_directory: relative path to directory from get_root_directory
        :param filename: filename only including extension


        :param data:
        :return:unique id
        """
        import fasty.JWT
        file_ext = os.path.splitext(filename)[-1][1:]
        file_id = bson.objectid.ObjectId(server_file_name_only)
        app_name = rel_path_to_directory.replace('\\','/').split('/')[0]
        upload_id = rel_path_to_directory.replace('\\','/').split('/')[1]
        db_name = await fasty.JWT.get_db_name_async(app_name)
        file_name = f"{server_file_name_only}.{file_ext}"
        if db_name is None:
            return None
        db = self.client.get_database(db_name)
        fs = GridFS(db)
        file = fs.find_one({"_id": file_id})
        if file is None:
            db.get_collection("fs.files").insert_one(
                {
                    "_id": file_id,
                    "chunkSize": data.__len__(),
                    "length": data.__len__(),
                    "filename": filename
                }
            )
            fs_chunks = db.get_collection("fs.chunks")
            fs_chunks.insert_one({
                "_id": bson.objectid.ObjectId(),
                "files_id": file_id,
                "n": 0,
                "data": data
            })

        else:

            chunk_index, m = divmod(file.length, file.chunk_size)
            file_len = file.length + data.__len__()
            db.get_collection("fs.files").update_one(
                {
                    "_id": file_id
                },
                {
                    "$set": {
                        "length": file_len
                    }
                }
            )
            fs_chunks = db.get_collection("fs.chunks")

            if m > 0:
                chunk_index += 1
            fs_chunks.insert_one({
                "_id": bson.objectid.ObjectId(),
                "files_id": file_id,
                "n": chunk_index,
                "data": data
            })

    async def read(self, file_stream, size):
        """
        Read a size of byte in stream from current position
        :param file_stream:
        :param read_size:
        :return:
        """
        return file_stream.read(size)

    async def get_stream(self, rel_path_to_file):
        """
        get stream of file content
        :param rel_path_to_file: relative path to file (root directory get by call get_root_directory
        :return:
        """
        import fasty.JWT
        str_mongoddb_file_id = os.path.splitext(rel_path_to_file.split('/')[-1])[0]
        app_name = rel_path_to_file.split('/')[0]
        db_name = await fasty.JWT.get_db_name_async(app_name)
        if db_name is None:
            return None
        mongoddb_file_id = bson.objectid.ObjectId(str_mongoddb_file_id)
        db = self.client.get_database(db_name)
        fs = GridFS(db)
        ret = fs.get(mongoddb_file_id)
        return ret

    async def get_len_of_file_stream(self, file_stream):
        """
        Get len of file stream
        :param file_stream:
        :return:
        """
        return file_stream.length

    async def open_stream(self, file_stream):
        """
        Open file stream.
        When file_stream was create maybe it was not open
        :param file_stream:
        :return:
        """
        if file_stream.closed:
            file_stream = GridFS(file_stream._GridOut__files.database).get(file_stream._id)
        return file_stream

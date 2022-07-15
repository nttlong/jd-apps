import pathlib
import uuid

from fasty.storage.must_impl import MustImplement
from fasty.storage.base_storage import base_storage
import os
from awaits.awaitable import awaitable


@MustImplement()
class file_storage(base_storage):
    def __init__(self, config_dir, yaml_path, data):
        self.config_data = data.get(self.get_key())
        self.location = self.config_data.get('location')
        if self.location is None:
            raise Exception(f"'{self.get_key()}.location' was not found in '{yaml_path}")
        if not os.path.isdir(self.location):
            raise Exception(f"'{self.location} was not found. Pleas, review '{yaml_path}'")

    def get_key(self):
        return "file"

    async def append_data(self, rel_path_to_directory: str, server_file_name_only: str, filename: str, data: bytes):
        file_id = server_file_name_only
        """
        Alloc a new file id. It will replace filename (original client file at client)
        """
        file_ext = os.path.splitext(filename)[-1][1:]
        """
        get extension of file
        """
        server_file_name = f"{file_id}.{file_ext}"
        """
        This is a real filename will be store at server
        """
        full_path_to_file = os.path.join(self.get_root_directory(), rel_path_to_directory, server_file_name).replace(
            '/', os.sep)
        """
        absolute path to file where upload file has been created 
        """
        full_path_to_directory = str(pathlib.Path(full_path_to_file).parent)
        if not os.path.isdir(full_path_to_directory):
            os.makedirs(full_path_to_directory)
        if not os.path.isfile(full_path_to_file):
            with open(full_path_to_file, "wb") as file:
                file.write(data)
        else:
            with open(full_path_to_file, "ab") as file:
                file.write(data)
        return file_id

    def get_root_directory(self) -> str:
        return self.location

    async def get_stream(self, rel_path_to_file):
        full_path_to_file = os.path.join(self.get_root_directory(), rel_path_to_file)
        if not os.path.isfile(full_path_to_file):
            return None
        return open(full_path_to_file, 'rb')

    async def read(self, file_stream, size):
        return file_stream.read(size)

    async def get_len_of_file_stream(self, file_stream):
        return os.path.getsize(file_stream.raw.name)

    async def open_stream(self, file_stream):
        if file_stream.closed:
            file_stream = open(file_stream.raw.name, 'rb')
        return file_stream

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
            raise Exception(f"'{self.location} was not found")

    def get_key(self):
        return "file"

    async def append_data(self, path_to_file, data: bytes):
        if not os.path.isfile(path_to_file):
            with open(path_to_file, "wb") as file:
                file.write(data)
        else:
            with open(path_to_file, "ab") as file:
                file.write(data)

    async def get_content(self, app_name: str, directory: str):
        chunk_size = 1024 * 1024
        full_path_to_file = os.path.join(self.location, app_name, directory).replace('/', os.sep)
        file_obj = open(full_path_to_file, 'rb')
        file_obj.seek(0)
        data = [1]
        while len(data) > 0:
            data = await file_obj.read(chunk_size)
            yield data
        file_obj.close()

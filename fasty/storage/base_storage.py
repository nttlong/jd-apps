from awaits.awaitable import awaitable


class base_storage:
    def __init__(self, config_dir: str, yaml_path, data: dict):
        """

        :param config_dir:
        :param yaml_path:
        :param data:
        """
        raise NotImplemented

    def get_key(self) -> str:
        raise NotImplemented

    async def get_content(self, app_name: str, directory: str):
        raise NotImplemented

    async def append_data(self, path_to_file, data: bytes):
        """
        Thêm nội dung vào file, nếu file chưa có tạo mới
        :param path_to_file:
        :param data:
        :return:
        """
        raise NotImplemented

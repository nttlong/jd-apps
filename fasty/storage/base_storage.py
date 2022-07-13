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

    def get_root_directory(self) -> str:
        """
        Get temp directory when user upload file
        :return:
        """
        raise NotImplemented

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
        raise NotImplemented
    async def read(self,file_stream,size):
        """
        Read a size of byte in stream from current position
        :param file_stream:
        :param read_size:
        :return:
        """
    async def get_stream(self, rel_path_to_file):
        """
        get stream of file content
        :param rel_path_to_file: relative path to file (root directory get by call get_root_directory
        :return:
        """
        raise NotImplemented

    async def get_len_of_file_stream(self, file_stream):
        """
        Get len of file stream
        :param file_stream:
        :return:
        """
        raise NotImplemented

    async def open_stream(self, file_stream):
        """
        Open file stream.
        When file_stream was create maybe it was not open
        :param file_stream:
        :return:
        """
        raise NotImplemented

# import os
#
#
# class file:
#     """
#     Chi tiết cấu hình lưu trữ dạng file
#     """
#
#     def __init__(self, config_dir: str, yaml_path, master_key: str, data: dict):
#         self.location = data.get('location')
#         """
#         Đường dẫn đến thư mục vật lý lưu file
#         """
#         if self.location is None:
#             raise Exception(f"{master_key}.location was not found in '{yaml_path}'")
#         if not os.path.isdir(self.location):
#             raise Exception(f"'{self.location}' was not found. Please preview '{yaml_path}' at '{master_key}.location'")
#         self.domain = data.get('domain')
#         if self.domain is None:
#             raise Exception(f"{master_key}.domain was not found in '{yaml_path}'")
#         self.username = data.get('username')
#         if self.username is None:
#             raise Exception(f"{master_key}.username was not found in '{yaml_path}'")
#         self.username = data.get('password')
#         if self.password is None:
#             raise Exception(f"{master_key}.password was not found in '{yaml_path}'")

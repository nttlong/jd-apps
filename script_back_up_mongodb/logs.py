import logging
logs =logging.getLogger("bk")
import pathlib
import os
current_dir= str(pathlib.Path(__file__).parent)
log_file_path = os.path.join(current_dir,"logs.txt")
formatter = logging.Formatter('%(asctime)s:%(levelname)s : %(name)s : %(message)s')
local_handler = logging.FileHandler(log_file_path)
local_handler.setFormatter(formatter)
logs.addHandler(local_handler)

logs.setLevel(logging.INFO)


logs.info("OK")
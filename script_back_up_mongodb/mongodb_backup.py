import logs
import config
import shutil
import datetime
import time
mongodb_dir=config.mongodb_dir

dump_proc=config.dump_proc

ouput_dr=config.ouput_dr

host = config.host

port =config.port

db=config.db

zip_folder = config.zip_folder

import os

if not os.path.isdir(mongodb_dir):
    raise Exception(f"{mongodb_dir} was not found")

full_dum_exec= os.path.join(mongodb_dir,dump_proc)

if not os.path.isfile(full_dum_exec):
    raise Exception(f"{full_dum_exec} was not found")

if not os.path.isdir(ouput_dr):
    raise Exception(f"{full_dum_exec} was not found")


if not os.path.isdir(zip_folder):
    raise Exception(f"{zip_folder} was not found")

logs.logs.info(config.__dict__)

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logs.logs.info('got line from subprocess: %r', line)

def run_backup_mongodb_command(ouput_dir_name):

    logs.logs.info("-----create mongdb dumb0-----------------")
    logs.logs.info(dict(
        host=host,
        port=port,
        db=db
    ))


    logs.logs.info("-----create mongdb dumb0-----------------")
    full_out_dir_name= os.path.join(ouput_dr,ouput_dir_name)
    if not os.path.isdir(full_out_dir_name):
        os.makedirs(full_out_dir_name)

    args =[
        #f"mongodb://{host}:{port}",
        f"--host={host}",
        f"--port={port}",
        f"--db={db}",
        f"--out={full_out_dir_name}"
    ]
    cmd=[full_dum_exec]+args
    from subprocess import Popen, PIPE, STDOUT
    process=Popen(cmd,stdout=PIPE, stderr=STDOUT)

    with process.stdout:
        log_subprocess_output(process.stdout)
    exitcode = process.wait()  # 0 means success
    if exitcode==0:
        logs.logs.info("-----create mongdb dumb is ok-----------------")
        logs.logs.info(dict(
            host=host,
            port=port,
            db=db
        ))

        logs.logs.info("-----create mongdb dumb-----------------")
        return full_out_dir_name
    else:
        logs.logs.info("-----create mongdb dumb is fail-----------------")
        logs.logs.info(dict(
            host=host,
            port=port,
            db=db
        ))

        logs.logs.info("-----create mongdb dumb-----------------")


def run_backup_mongdb_then_zip(ouput_dir_name):
    try:
        ret= run_backup_mongodb_command(ouput_dir_name)
        output_filename =os.path.join(zip_folder,f"{ouput_dir_name}")
        shutil.make_archive(output_filename, 'zip', ret)
    except Exception as e:
        logs.logs.debug(e)
    finally:
        return

while True:
    time.sleep(10)
    back_up_time = datetime.datetime.now()
    h = back_up_time.hour
    if h>0:
        ouput_dir_name = back_up_time.strftime("%Y-%m-%d")
        run_backup_mongdb_then_zip(ouput_dir_name)





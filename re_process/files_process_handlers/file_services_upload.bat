@echo off
chcp 1252
set run_path=C:\dj-apps-2022-05-25\jd-apps
set venv_dir=venv
cd "%run_path%\%venv_dir%"
echo %run_path%\%venv_dir%\scripts\activate.bat
call %run_path%\%venv_dir%\scripts\activate.bat
python %run_path%\re_process/files_process_handlers/files_services_upload.py

"""
Đễ chạy được FastAPI ở chế độ deploy ra intrenet
iis sẽ dùng Fastcgi để start file này
"""
import sys
import pathlib
import fasty
import os
fasty.load_config(os.environ["PYTHONPATH"],"uvicorn.error")
import api_app
from a2wsgi import ASGIMiddleware
fasty.config.logger.info("Web api run on iis start")



wsgi_app = ASGIMiddleware(api_app.app)

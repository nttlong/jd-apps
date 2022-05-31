import os
import re

import gridfs
from flask import render_template, request, Blueprint, current_app, send_file,Response

core = Blueprint("core", __name__)

# your request handles here with @core.route()


# @core.route("/")
# def home():
#     return render_template("index.html")

FEED_SIZE=1024*1024
# @core.route("/video", methods=["GET"])
def video(fs,mime_type):
    assert isinstance(fs,gridfs.GridOut)
    headers = request.headers
    if not "range" in headers:
        fs.seek(0, os.SEEK_SET)
        data = fs.read(FEED_SIZE)
        res = Response(data, status=206, mimetype=mime_type)
        # res.headers.add("Accept-Ranges", "bytes")
        res.headers.add("Content-Range", f"bytes {0}-{fs.length - 1}/{fs.length}")
        # Content-Range: bytes 0-1077614590/1077614591
        # res.headers.add("Content-Length", f"{fs.length}")
        return res

    # video_path = os.path.abspath(os.path.join("media", "test.mp4"))
    size = fs.length
    # size = size.st_size
    # if  not range_header:
    #
    chunk_size = 10**3
    start = int(re.sub("\D", "", headers["range"]))
    end = min(start + chunk_size, size - 1)

    content_lenght = end - start + 1

    def get_chunk(start, end):
        fs.seek(start,os.SEEK_SET)
        chunk = fs.read(end)
        fs.close()
        return chunk

    headers = {
        "Content-Range": f"bytes {start}-{size-1}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": content_lenght,
        "Content-Type": "video/mp4",
    }
    res =current_app.response_class(get_chunk(start, end), 206, headers)
    return res
import mimetypes
import os
import re

import gridfs
from flask import request, stream_with_context, Response,make_response,current_app




FEED_SIZE=1024*2
def send_file_partial(fs,request,mime_type):
    """
        Simple wrapper around send_file which handles HTTP 206 Partial Content
        (byte ranges)
        TODO: handle all send_file args, mirror send_file's error handling
        (if it has any)
    """
    assert isinstance(fs,gridfs.GridOut)
    def generate():
        r =[1]
        while r.__len__()>0:
            r = fs.read(1000)
            yield r
    range_header = request.headers.get('Range', None)
    size = fs.length
    if  not range_header:
        fs.seek(0,os.SEEK_SET)
        data = fs.read(FEED_SIZE)
        res= Response(data,status=206,mimetype=mime_type)
        # res.headers.add("Accept-Ranges", "bytes")
        res.headers.add("Content-Range", f"bytes {0}-{size-1}/{size}")
        #Content-Range: bytes 0-1077614590/1077614591
        res.headers.add("Content-Length", f"{size}")
        return res


    byte1, byte2 = 0, None

    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()

    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1
    # length = min(length,1024*1024)
    data = None
    def read_data():
        yield_data=[]
        fs.seek(byte1)
        bdd = fs.read(FEED_SIZE)
        yield_data += bdd
        while bdd.__len__()>0:
            bdd = fs.read(FEED_SIZE)
            yield_data+=bdd
            yield yield_data

    headers = {
        "Content-Range": f"bytes {byte1}-{size - 1}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": size,
        "Content-Type": "video/mp4",
    }

    return current_app.response_class(read_data(), 206, headers)
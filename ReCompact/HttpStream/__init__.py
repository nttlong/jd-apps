import os
import re
import mimetypes
from wsgiref.util import FileWrapper
import gridfs
from django.http.response import StreamingHttpResponse

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=2097152, offset=0, length=None):
        fs = filelike

        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        if length is None:
            self.remaining = fs.length - offset-fs.tell()
        else:
            self.remaining = fs.length
        self.blksize = blksize
        self.next_blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            print("self.filelike.close")
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        import asyncio
        def read_async():

            if self.remaining is None:
                # If remaining is None, we're reading the entire file.

                data = self.filelike.read(self.blksize)
                if data:
                    return data

            else:
                if self.remaining <= 0:
                    return None
                data = self.filelike.read(min(self.remaining, self.blksize))
                if not data:
                    return None

                self.remaining -= len(data)
                return data

        from multiprocessing.pool import ThreadPool
        pool = ThreadPool(processes=4)

        async_result = pool.apply_async(read_async, ())  # tuple of args for foo

        # do some other stuff in the main process

        return_val = async_result.get()  #
        if return_val is None:
            raise StopIteration()

        # loop = asyncio.get_event_loop()
        # coroutine = th()
        # r = loop.run_until_complete(coroutine)
        # r= read_async()
        return return_val
        #
        #
        # if self.remaining is None:
        #     # If remaining is None, we're reading the entire file.
        #
        #     data = self.filelike.read(self.blksize)
        #     if data:
        #         return data
        #     raise StopIteration()


def streaming_mongo_db_fs(request, file: gridfs.grid_file.GridOut):
    assert isinstance(file, gridfs.grid_file.GridOut), 'file_must be gridfs.grid_file.GridOut'
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = file.length
    content_type, encoding = mimetypes.guess_type(file.filename)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(file, offset=first_byte, length=length), status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(file),                                     content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
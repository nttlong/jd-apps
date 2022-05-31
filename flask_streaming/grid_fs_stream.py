import gridfs
from flask import Response, stream_with_context
import os

def streaming_content(fs:gridfs.GridOut,mime_type:str,request,chunk_size=1024*32):
    """
    Streaming nội dung
    :param fs: Có thể là một file vật lý, hoặc 1 file trong mongodb, vân vân và mây mây
    Miễn sao có hỗ reo75 dạng seekable là ok
    :param mime_type:
    :param request:
    :return:
    """


    def generate():
        """
        Read content from fs, đọc hế nôi dung của file
        Đừng lo về độ lớn của file vì đang chạy ở chế độ yeild

        :return:
        """
        chunk = chunk_size
        data = [1]
        while data.__len__() > 0:
            data = fs.read(chunk)
            yield data
        fs.close()

    def read_from_to(start, end):
        """
        Đọc từng đoạn theo yêu cầu
        :param start:
        :param end:
        :return:
        """
        def yeild_list():
            yeild_size =1024*32
            fs.seek(start, os.SEEK_SET)
            leng_of_bytes= end-start
            n = int(leng_of_bytes/yeild_size)
            if leng_of_bytes % yeild_size>0:
                n+=1

            remain = leng_of_bytes
            r_size = min(yeild_size,remain)
            for i in range(0,n):
                y_data = fs.read(r_size)
                remain-= y_data.__len__()
                r_size = min(yeild_size, remain)
                if y_data is None:
                    yield b''
                else:
                    yield y_data


        return yeild_list()

    from flask import make_response
    if not request.range:
        """
        When the firsttime client device request 
        Lần đầu thiết bị trình chiếu nội dung
        Client Device sẽ thăm dò hết nôi dung
        Đùng quá lo lắng về dung lương đọc
        Vì reong đoạn này đang gọi hàm generate ở chế độ yeild 
        """
        res = Response(stream_with_context(generate()), status=200, mimetype=mime_type)
        res.headers.add("Accept-Ranges", "bytes")
        """
        Báo cho thiết bị biết chấp nhận đọc the range
        """
        res.headers.add("Content-Length", f"{fs.length}")
        """
        Báo cho Client Device biết độ dài của nội dung
        """
        res.headers.add("Content-Range", f"bytes {0}-{fs.length - 1}/{fs.length}")
        """
        Báo cho thiết bị biết phạm vi củ nôi dung
        """
        return res
    if request.range and request.range.ranges[0][1] is None and request.range.ranges[0][0] == 0:

        res = Response(stream_with_context(generate()), status=206, mimetype=mime_type)

        res.headers.add("Content-Length", f"{fs.length}")
        """
        """
        res.headers.add("Content-Range", f"bytes {0}-{fs.length - 1}/{fs.length}")
        return res
    if request.range and request.range.ranges[0][1] is None and request.range.ranges[0][0] > 0:
        """
                Sau khi thăm dò nội dung xong 
                Nếu đây là video hoặc audio thiết bị sẽ đọc phần cuối của nội dung
                nhằm xác định nội dung có hơp lệ hay không
                Độ dài phần cuối này thường là 354203 bytes với Video
                Audio thì tìm kiếm trên mạng mà xem hoặc upload thử file mp3 rồi debug
        """
        start = request.range.ranges[0][0]
        end = fs.length

        res = Response(stream_with_context(read_from_to(start, end)), status=206, mimetype=mime_type)
        res.headers.add("Content-Length", f"{fs.length - start}")
        res.headers.add("Content-Range", f"bytes {start}-{end - 1}/{fs.length}")
        return res
    else:
        raise Exception()
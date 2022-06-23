import datetime
import threading

import uuid
from queue import Queue


class ThreadCommunicator:
    """
    Cấu trúc này dùng để giao tiếp các thread
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.meta = dict()
        self.action = ''
        self.status = ''
        self.start_on=None
        self.q = Queue()
        self.thread: threading.Thread = None
        self.tracking =[]

    def post_message(self,action,status:int, data):

        if status == 1:
            item = None
            for x in self.tracking:
                if x.get('action')==action:
                    item = x
                    break

            if item:
                item= self.tracking[self.tracking.__len__()-1]
                item['end_on']= datetime.datetime.utcnow()
                item['complete_time_in_second'] = (item['end_on'] - item['start_on']).total_seconds()
            else:
                self.tracking+=[
                    dict(
                        start_on= datetime.datetime.utcnow(),
                        action = action,
                        status =status
                    )
                ]
        else:
            self.tracking += [
                dict(
                    start_on=datetime.datetime.utcnow(),
                    action=action,
                    status=status
                )
            ]
        self.meta = data
        self.action = action
        self.status = status
        self.meta=data

    def get_return_value(self):
        r = self.q.get()
        return r


def hooker(communicator: ThreadCommunicator, *args, **kwargs):
    if not issubclass(type(communicator), ThreadCommunicator):
        raise Exception('communicator must be a subclass of ThreadCommunicator')

    def wrapper(*a, **kwa):
        fn = a[0]
        if callable(fn):
            def th_runner(*x, **y):
                def excutor(u, v):
                    communicator.q.put(fn(*u, **v))

                communicator.thread = threading.Thread(target=excutor, args=(x, y))

                fx = communicator.thread.start()

            return th_runner

    return wrapper



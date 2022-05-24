"""
Consumer for upload file
Everytime when files.services is upload with successful producer 'file_upload' topic
How to use:
    import re_process.consum_upload_file
    re_process.consum_upload_file.int(

    )
"""

__consumer__ = None
__on_process__ = None
__on_error__ = None


def init(config, on_process,on_error):
    import ReCompact_Kafka.consumer
    global __consumer__
    global __on_error__
    global __on_process__
    assert callable(on_process),'on_process must be a function'
    assert callable(on_error), 'on_error must ne a function'
    assert on_process.__code__.co_argcount ==1, 'Thee must declare on_process with on param'
    assert on_error.__code__.co_argcount == 1, 'Thee must declare on_error with on param'

    __on_error__ =on_error
    __on_process__ = on_process
    __consumer__ = ReCompact_Kafka.consumer.Consumer_obj(config)

def start():
    import ReCompact_Kafka.consumer
    global __consumer__
    assert isinstance(__consumer__,ReCompact_Kafka.consumer.Consumer_obj),'error __consumer__ mus be ReCompact_Kafka.consumer.Consumer_obj'
    global __on_error__
    global  __on_process__
    __consumer__.watch_topic(
        topic_key="files.services.upload",
        on_error= __on_error__ ,
        handler=  __on_process__
    )


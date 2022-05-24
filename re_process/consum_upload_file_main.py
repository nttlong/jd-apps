import consum_upload_file


def error_topic(msg):
    fx = msg
    print(fx)

def process_topic(msg):
    fx = msg
    print(fx)




consum_upload_file.init(
    config= {
        'bootstrap.servers': '192.168.18.36:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False
    },
    on_error= error_topic,
    on_process= process_topic
)

consum_upload_file.start()

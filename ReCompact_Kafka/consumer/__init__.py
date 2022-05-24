from confluent_kafka import Consumer
import asyncio

import threading


class Consumer_obj(Consumer):
    """
    Conusmer_obj inherit form confluent_kafka.Consumer
    """

    def __init__(self, topic, on_consum, on_consum_error, *args, **kwargs):
        self.topic = topic
        self.on_consum = on_consum
        self.on_consum_error = on_consum_error
        if isinstance(args, tuple):
            self.config = args[0]
            self.broker=args[0]['bootstrap.servers'].split(',')
        super().__init__(*args, **kwargs)

    def get_all_topics_keys(self):
        import confluent_kafka.admin
        meta = self.list_topics()
        assert isinstance(meta, confluent_kafka.admin.ClusterMetadata)
        return meta.topics

    def get_json(self, msg):
        import json
        msg_value_dict = json.loads(
            msg.value().decode("utf-8")
        )
        return msg_value_dict

    def get_topic_id(self, msg):
        return msg.topic()

    def __watch_topic__(self, topic_key, handler, on_error) -> threading.Thread:
        def run(o, tk, h, e):
            o.subscribe([tk])
            while True:
                msg = o.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if callable(on_error):
                        e(msg)
                    continue
                if callable(handler):
                    """
                    Quan trọng, chỗ này tạo thread để chạy
                    """
                    import threading
                    run_th = threading.Thread(
                        target=h,
                        args= (
                            o,msg,
                        )
                    )
                    run_th.start()
                    run_th.join()

        ret = threading.Thread(
            target=run,
            args=(
                self,
                topic_key,
                handler,
                on_error
            )
        )
        return ret

    def get_thread(self):
        return self.__watch_topic__(
            self.topic,
            self.on_consum,
            self.on_consum_error

        )


"""
_config = {
    'bootstrap.servers': "'".join(re_process.config.kafka_broker),
    'group.id': f'client.files.services.process.{g_id}',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}
"""


def create(
        server,
        group_id,
        topic_id,
        on_consum,
        on_consum_error
) -> Consumer_obj:
    return Consumer_obj(
        topic_id,
        on_consum,
        on_consum_error,
        {
            'bootstrap.servers': ",".join(server),
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False

        }
    )

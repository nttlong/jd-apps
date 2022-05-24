from confluent_kafka import Consumer
import asyncio


class Consumer_obj(Consumer):
    def __init__(self, *args, **kwargs):
        if isinstance(args,tuple):
            self.config =args[0]
        super().__init__(*args, **kwargs)

    def get_all_topics_keys(self):
        import confluent_kafka.admin
        meta = self.list_topics()
        assert isinstance(meta, confluent_kafka.admin.ClusterMetadata)
        return meta.topics

    def watch_topic(self, topic_key, handler, on_error):
        self.subscribe([topic_key])
        while True:
            msg = self.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if callable(on_error):
                    on_error(msg)
                continue
            if callable(handler):
                handler(msg)

        self.close()



"""
How to use:
    1- Thee must create new Bootstrap with broker server in initial parameters, then assign to one variable.
    The variable can be use across thy application. If thy call Bootstrap again with the same broker server
    Thee will get old instance
    2- In order create a new topic just call <boostrap server variable>.producers.<topic name>.send(<dict data>)

    Example:
        my_brokers= new Bootstrap(["server 1:port1"],...)
        my_brokers.producers.topics.hello_world.topic.send({"Name":"znazi"})
        or
        getattr(my_brokers.producers.topics,"hello_world").topic.send({"Name":"znazi"})
    Example 2 print topic key:
        purchase_topic = my_brokers.producers.topics.purchase
        print(purchase_topic.topic_key) show "purchase"
        order_topic = purchase.topics.topic.order
        print(order_topic.topic_key) show "purchase.order"




"""




__static_dict__ = None

import confluent_kafka
import threading as __threading__

__lock__ = __threading__.Lock()


class KafkaProducerAuto():
    def __init__(self, topic_key, bootstrap_servers):
        import json
        import time
        self.__producer__ = None
        is_ok = False
        self.bootstrap_servers = bootstrap_servers
        while not is_ok:
            try:
                self.__producer__ = confluent_kafka.Producer(
                    {
                        'bootstrap.servers': ",".join(self.bootstrap_servers)
                        # 'socket.timeout.ms': 100,
                        # 'api.version.request': 'false',
                        # 'broker.version.fallback': '0.9.0',
                    }
                )

                is_ok = True
            except Exception as e:
                time.sleep(0.3)

        self.topic_key = topic_key
        self.topic = KafkaProducerAuto.__Topic__(self)

    class __Topic__:
        def __init__(self, owner):
            self.__owner__ = owner

        def __getattr__(self, item):

            return KafkaProducerAuto.__Topic__.__Sender__(
                self.__owner__.topic_key + "." + item,
                self
            )

        class __Sender__:
            def __init__(self, topic_key, owner):
                self.__owner__ = owner
                self.topic_key = topic_key

            def send(self, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
                import json
                from bson import json_util
                assert isinstance(self.__owner__, KafkaProducerAuto.__Topic__)
                assert isinstance(self.__owner__.__owner__, KafkaProducerAuto)

                def delivery_report(err, msg):
                    if err:
                        print(err)
                    else:
                        print(msg)

                ret = self.__owner__.__owner__.__producer__.produce(
                    self.topic_key,
                    json.dumps(value, check_circular=False, default=json_util.default),
                    callback=delivery_report

                )

                return ret


Topic_sender = KafkaProducerAuto.__Topic__.__Sender__


def __producer__(
        producer_name,
        servers
):
    global __static_dict__
    global __lock__
    assert isinstance(producer_name, str), 'producer_name must be str'
    assert isinstance(servers, list), 'producer_name must be str[]'

    producer_name = producer_name.lower()
    from confluent_kafka import Producer

    import json
    if not __static_dict__:
        __lock__.acquire()
        __static_dict__ = {}
        __lock__.release()
    ret = __static_dict__.get(producer_name, None)

    if not isinstance(ret, Producer):
        __lock__.acquire()
        ret = Producer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        __lock__.release()
    return ret


class Bootstrap:

    def __init__(self, bootstrap_servers):
        """
        Create bootstrap servers
        """
        assert isinstance(bootstrap_servers, list), 'producer_name must be str[]'
        self.__bootstrap_servers__ = bootstrap_servers
        self.producers = Bootstrap.ReProducer(self)

    class ReProducer:
        def __init__(self, owner):
            self.__owner__ = owner

        # def __getitem__(self, item):
        #     print("get_" + item)
        # def __getattr__(self, item):
        #     print("get_"+item)
        def __getattr__(self, item):
            assert isinstance(self.__owner__, Bootstrap)
            return KafkaProducerAuto(item, self.__owner__.__bootstrap_servers__)

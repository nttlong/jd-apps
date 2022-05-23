from confluent_kafka import Consumer


c = Consumer({
    'bootstrap.servers': '192.168.18.36:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit':False
})

ls = c.list_topics()
print(ls)
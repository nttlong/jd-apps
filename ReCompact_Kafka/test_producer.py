import producer
bootstrap = producer.Bootstrap(
    ["192.168.18.36:9092"]
)
ff =bootstrap.producers
getattr(ff.topics.topic,"hello world").send({"name":"myname"})
print(ff)
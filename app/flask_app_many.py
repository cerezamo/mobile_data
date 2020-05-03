from flask import Flask, render_template, Response
from pykafka import KafkaClient
#from flask_caching import Cache

#  $KAFKA/bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic antennos --config retention.ms=5000 
#cache = Cache(config={'CACHE_TYPE': 'simple'})

def get_kafka_client():
    return KafkaClient(hosts='localhost:9092')

app = Flask(__name__)
#cache.init_app(app)

@app.route('/')
#@cache.cached(timeout=50)
def index():
    """Serve the index HTML"""
    return(render_template('index_many_test_spark.html'))

 #Consumer API

@app.route('/topic/antennesOutput')
def get_messages():
    client = get_kafka_client()
    def events():
        liste = []
        j = 0
        for i in client.topics['antennesOutput'].get_simple_consumer():
            liste.append(i.value.decode())
            j ++
        string = ''
        for i in range(j):
            string += 'data:{0}\n\n'.format(liste[i])
        yield string
    return Response(events(), mimetype="text/event-stream")

# @app.route('/topic/antennos')
# def get_messages():
#     #client = KafkaClient(hosts='127.0.0.1:9092')
#     client = KafkaClient(hosts='localhost:9092')

#     topic = client.topics["antennos"]
#     def events():
#         i = topic.get_simple_consumer()
#         yield 'data:{0}\n\n'.format(i.value.decode())
#     return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(port=2000,use_reloader=True) # 
    #socketio.run(app)
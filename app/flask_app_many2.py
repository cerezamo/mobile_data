# from flask import Flask, render_template, Response
# from pykafka import KafkaClient


# def get_kafka_client():
#     return KafkaClient(hosts='localhost:9092')


# client = get_kafka_client(auto_offset_reset=OffsetType.LATEST,reset_offset_on_start=True)
# import time 
# time.sleep(2)
# message_list = pd.DataFrame(columns=['PhoneID','x','y'])
# for i in client.topics['antennesOutput'].get_simple_consumer():
#     data= json.loads(i.value.decode())
#     data_frame = pd.DataFrame([data['PhoneId'],data['x'],data['y']]).transpose()
#     data_frame.columns = ['PhoneID','x','y']
#     message_list = pd.concat([message_list,data_frame],axis=0)
#     print(message_list)



from flask import Flask, render_template, Response
from pykafka import KafkaClient
import flask

from flask_caching import Cache

# $KAFKA/bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic antennos --config retention.ms=5000 
cache = Cache(config={'CACHE_TYPE': 'simple'})

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

# @app.route('/topic/antennesOutput')
# def get_messages():
#     client = get_kafka_client()
#     def events():
#         res = {"messages" : []}
#         for message in client.topics['antennesOutput'].get_simple_consumer():
#             res["messages"].append(message.value.decode("utf-8"))
#         res = flask.jsonify(res)
#         yield 'res:{0}\n\n'.format(res)
#     return Response(events(), mimetype='application/json') # mimetype="text/event-stream"

@app.route('/topic/antennesOutput')
def get_messages():
    client = get_kafka_client()
    def events():
        #res = {"messages" : []}
        for message in client.topics['antennesOutput'].get_simple_consumer():
            res = message.value.decode()
            yield 'data:{0}\n\n'.format(res)
            #res["messages"].append(message.value.decode())
        #res = flask.jsonify(res)
    return Response(events(), mimetype="text/event-stream") # mimetype="text/event-stream"'application/json' text/event-stream

# @app.route('/topic/antennos')
# def get_messages():
#     #client = KafkaClient(hosts='127.0.0.1:9092')
#     client = KafkaClient(hosts='localhost:9092')

#     topic = client.topics["antennos"]
#     def events():
#         i = topic.get_simple_consumer()
#         yield 'data:{0}\n\n'.format(i.value.decode())
#     return Response(events(), mimetype="text/event-stream")


# @app.route('/topic/antennesOutput')
# def get_messages():
#     client = get_kafka_client()
#     def events():
#         res = {"messages" : []}
#         for i, message in enumerate(client.topics['antennesOutput'].get_simple_consumer()):
#             yield 'data:{0}\n\n'.format(i.value.decode())
#     return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(port=2000,use_reloader=True) # 
    #socketio.run(app)
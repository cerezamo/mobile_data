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
    return(render_template('index_many_simple.html'))


@app.route('/topic/antennes_static')
def get_data():
  return app.send_static_file('antennes.json')

@app.route('/topic/antennesOutput')
def get_messages():
    client = get_kafka_client()
    def events():
        import time
        res = {}
        for message in client.topics['antennesOutput'].get_simple_consumer():
            import json
            key = str(json.loads(message.value.decode())["PhoneId"])
            res[key] = json.loads(message.value.decode())
            output=json.dumps(res)
            yield 'data:{0}\n\n'.format(output)
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
from flask import Flask, render_template, Response
from pykafka import KafkaClient

def get_kafka_client():
    return KafkaClient(hosts='localhost:9092')

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the index HTML"""
    return(render_template('index2.html'))

 #Consumer API

@app.route('/topic/antennos')
def get_messages():
    client = get_kafka_client()
    def events():
        for i in client.topics['antennos'].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
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
    app.run(port=1995,use_reloader=True) # 

    #socketio.run(app)
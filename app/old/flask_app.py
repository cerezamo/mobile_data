from flask import Flask, render_template, Response
from pykafka import KafkaClient

def get_kafka_client():
    return KafkaClient(hosts='localhost:9092')

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

#Consumer API
@app.route('/izi')
def get_messages():
    client = KafkaClient(hosts='127.0.0.1:9092')
    topic = client.topics["antennes"]
    def events():
        i = topic.get_simple_consumer()
        yield 'data:{0}\n\n'.format(str(i.value.decode()))
    return Response(events())

if __name__ == '__main__':
    app.run(debug=True, port=5001)
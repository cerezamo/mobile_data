from pykafka import KafkaClient

client = KafkaClient(hosts="127.0.0.1:9092")

#print(client.topics)
topic = client.topics['antennes']
consumer = topic.get_simple_consumer()
# for message in consumer:
# 	if message is not None:
# 		print(message.value.decode('ascii'))

from flask import Flask, Response
app = Flask(__name__)


@app.route('/')
def get_message():
	def events():
		for message in consumer:
			yield "data:{0}\n\n".format(message.value.decode('ascii'))
	return Response(events())

if __name__ == "__main__":
	app.run(debug=True, port=5001)
	

from pykafka import KafkaClient
from pymongo import MongoClient
import json

def get_kafka_client():
    return KafkaClient(hosts='localhost:9092')

client_kafka = get_kafka_client()
consumer = client_kafka.topics['antennesOutput'].get_simple_consumer()

client_mongo = MongoClient('localhost:27017')
collection = client_mongo.mobiledata.antennes

for message in consumer:
	message = json.loads(message.value.decode())
	key = str(message["PhoneId"])
	collection.update_one({'PhoneId': key},
							{'$set':
							 {
								 'x': float(message['x']),
								 'y': float(message['y'])
							 }
							},
						 upsert=True)
	# print('{} added to {}'.format(message, collection))
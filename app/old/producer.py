
from pykafka import KafkaClient
import json 
from datetime import datetime
import time
import uuid 
import pandas as pd

input_file= pd.read_csv('/home/cerezamo/projet_stream/simulator/mobile_data/kafka_ingestion.csv')

client = KafkaClient(hosts="localhost:9092")
topic=client.topics['antennesInput']
producer = topic.get_sync_producer()

input_file = input_file[['PhoneId','x','y']]

data = {}

data['text'] = input_file['PhoneId']
data['x'] = input_file['x'][1]
data['y'] = input_file['y'][1]

def generate_checkpoint(input_file):
    i = 0
    while i < len(input_file):
        data['text'] = str(input_file['PhoneId'][i])
        data['x'] = input_file['x'][i]
        data['y'] = input_file['y'][i]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(5)
        i+=1
        
generate_checkpoint(input_file)
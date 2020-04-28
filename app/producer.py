
from pykafka import KafkaClient
import json 
from datetime import datetime
import time
import uuid 
import pandas as pd

input_file= pd.read_csv('/home/cerezamo/projet_stream/simulator/mobile_data/kafka_minimal_df.csv')



client = KafkaClient(hosts="localhost:9092")
topic=client.topics['antennos']
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
        data['x'] = input_file['x'][i]/1000
        data['y'] = input_file['y'][i]/1000
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(0.2)
        i+=1
        
generate_checkpoint(input_file)
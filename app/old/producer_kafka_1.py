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

input_file = input_file[['t','PhoneId','x','y']]

input_file.PhoneId = input_file.PhoneId.astype(str)
input_file.x = input_file.x/1000
input_file.y = input_file.y/1000

def generate_checkpoint(input_file):
    for i in range(0,input_file.t.max()):
        input_file_topush = input_file[input_file.t==i]
        message = input_file_topush.to_json(orient='records')
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)
        
generate_checkpoint(input_file)
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

data = {'x' : [] , 'y' : [] , 'text' : []}

def generate_checkpoint(input_file):
    for i in range(0,input_file.t.max()):
        input_file_topush = input_file[input_file.t==i]
        data = {'x' : [] , 'y' : [] , 'text' : []}
        
        j=0
        while j < len(input_file_topush):
            data['text'].append(input_file['PhoneId'][j])
            data['x'].append(input_file['x'][j]/1000)
            data['y'].append(input_file['y'][j]/1000)
            j+=1
            
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(3)
        
generate_checkpoint(input_file)
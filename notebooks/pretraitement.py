###################################################################
################# Préparer le fond de carte Plotly #################
###################################################################

import os 
import pandas as pd
from shapely.geometry import Point, Polygon
from shapely import wkt
import geopandas
import json
os.chdir('../madrid_sim') #If clone into "simulator"

Antenne_Info=pd.read_csv('AntennaInfo_MNO_MNO1.csv') # Open csv
Antenne_Info.columns=['t','Antenna_Id','Event_code','Device_ID','x','y','Tile_ID'] #Set column names
Antenne_Info=Antenne_Info[['Antenna_Id','x','y']] # Keep interesting stuff
Antenne_Info=Antenne_Info.drop_duplicates(ignore_index=True) # drop duplicates
Antenne_Info=Antenne_Info.drop_duplicates(subset=['x','y'],ignore_index=True)
Antenne_Info=Antenne_Info.drop_duplicates(subset=['Antenna_Id'],ignore_index=True)
Antenne_Info=Antenne_Info.sort_values('Antenna_Id',ignore_index=True)
Antenne_Info.to_json('../app/static/antennes.json',orient='records')

###################################################################
################# Préparer la base d'input Kafka ##################
###################################################################
import re
import datetime
from datetime import datetime, timedelta

DATA_PATH = os.getcwd()
files = [f for f in os.listdir(DATA_PATH) if (os.path.isfile(os.path.join(DATA_PATH, f)) and re.match('\\d_MNO_MNO1.csv', f[-14:]))]

data = pd.DataFrame(columns=['t','AntennaId','EventCode','PhoneId','x','y','TileId'])
for file in files:
    data_to_append = pd.read_csv(file)
    data=data.append(data_to_append)
    
data.PhoneId = data.PhoneId.astype(str)
base = datetime.now()
time_list = [base + timedelta(minutes=i) for i in range(len(data.t.unique()))]
time_list = [t.strftime("%m-%d-%Y %H:%M:%S") for t in time_list]
mergetime = pd.concat([pd.DataFrame(data.t.unique()),pd.DataFrame(time_list)],axis=1)
mergetime.columns =['t','timestamp']
data = data.merge(mergetime,on='t')
data.to_csv('../kafka_ingestion.csv',index=False,header=True)
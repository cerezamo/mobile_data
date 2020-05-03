import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 pyspark-shell'
import pyspark
import os
import re
from kafka import SimpleProducer, KafkaClient
from kafka import KafkaProducer
from pyspark.streaming import StreamingContext
from pyspark.sql import Column, DataFrame, Row, SparkSession
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkConf, SparkContext
import time 
# spark = SparkSession.builder \
#   .appName("Spark Structured Streaming from Kafka") \
#   .getOrCreate()
DATA_PATH = '/home/cerezamo/projet_stream/simulator/mobile_data/madrid_sim/'
files = [f for f in os.listdir(DATA_PATH) if (os.path.isfile(os.path.join(DATA_PATH, f)) and re.match('\d_MNO_MNO1.csv', f[-14:]))]
sc = pyspark.SparkContext().getOrCreate()
sqlContext = pyspark.SQLContext(sc)
#producer = KafkaProducer(bootstrap_servers='server.kafka:9092') # 2181
from pyspark.sql.types import *
schema = StructType([StructField("t", IntegerType(), True), 
                     StructField("AntennaId", IntegerType(), True), 
                     StructField("EventCode", IntegerType(), True),
                     StructField("PhoneId", IntegerType(), True), 
                     StructField("x", FloatType(), True),
                     StructField("y", FloatType(), True),
                     StructField("TileId", IntegerType(), True)
                   ])
main_df = sqlContext.read.csv(os.path.join(DATA_PATH, files[0]), header=True, schema=schema)
for i in range (1, len(files)):
    sc.addFile(os.path.join(DATA_PATH, files[i]))
    main_df = main_df.union(sqlContext.read.csv(DATA_PATH + files[i], header=True ,inferSchema=True,schema=schema))

main_df = main_df.where("EventCode!=1")
main_df = main_df.select([c for c in main_df.columns if c in ['t','PhoneId','x','y']])  
main_df = main_df.orderBy('t', ascending=True)
main_df = main_df.withColumn('x', main_df.x/1000).withColumn('y', main_df.y/1000)

query = main_df \
  .selectExpr("CAST(t AS STRING) AS key", "to_json(struct(*)) AS value") \
  .write  \
  .partitionBy('t') \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "antennos") \
  .save()
  # Envoie un par un >< 

# for i in range(0,1): # main_df.select('t').rdd.max()[0]
#   main_df \
#   .select(main_df['t'] ==i) \
#   .selectExpr("CAST(t AS STRING) AS key", "to_json(struct(*)) AS value") \
#   .write \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "localhost:9092") \
#   .option("topic", "antennos") \
#   .save()
    
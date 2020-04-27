import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 pyspark-shell'

from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName("Spark Structured Streaming from Kafka") \
  .getOrCreate()

################ PARTIE PREPARATION #################

# Création de la structure de nos données
from pyspark.sql.types import *

schema_ant = StructType([StructField("t", IntegerType()),
                     StructField("AntennaId", IntegerType()),
                     StructField("EventCode", IntegerType()),
                     StructField("PhoneId", IntegerType()),
                     StructField("x", FloatType()),
                     StructField("y", FloatType()),
                     StructField("TileId", IntegerType()) ])


from pyspark import Row
  
# Function to upsert `microBatchOutputDF` into Delta table using MERGE
def upsertToDelta(microBatchOutputDF, batchId): 
  # Set the dataframe to view name
  microBatchOutputDF.createOrReplaceTempView("updates")

  # ==============================
  # Supported in DBR 5.5 and above
  # ==============================

  # Use the view name to apply MERGE
  # NOTE: You have to use the SparkSession that has been used to define the `updates` dataframe
  microBatchOutputDF._jdf.sparkSession().sql("""
    MERGE INTO aggregates t
    USING updates s
    ON s.key = t.key
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
  """)

# Setting # partitions to 1 only to make this demo faster.
# Not recommended for actual workloads.
spark.conf.set("spark.sql.shuffle.partitions", "1")

# Reset the output aggregates table
spark.createDataFrame([ Row(key=0, count=0) ]).write \
  .format("delta").mode("overwrite").saveAsTable("aggregates")



################ PARTIE STREAM ######################


sdfAntennes = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "antennes") \
  .option("startingOffsets", "latest") \
  .load() \
  .selectExpr("CAST(value AS STRING)")

def parse_data_from_kafka_message(sdf, schema):
    from pyspark.sql.functions import split
    assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
    col = split(sdf['value'], ',')
    for idx, field in enumerate(schema):
        sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    sdf = sdf.select([field.name for field in schema])
    return  sdf

sdfAntennes = parse_data_from_kafka_message(sdfAntennes, schema_ant) \
			  .orderBy('t', ascending=False) \
			  .coalesce(1) \
			  .dropDuplicates(subset = ['PhoneId'])

df_main = sdfAntennes.writeStream.outputMode("update").format("console").start().awaitTermination()



# query = sdfAntennes.writeStream.format("console").start()
# query = sdfAntennes.groupBy("AntennaId").count()
# query.writeStream.outputMode("complete").format("console").start().awaitTermination()
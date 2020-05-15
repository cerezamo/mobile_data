import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 pyspark-shell'

################ PARTIE PREPARATION #################

import pyspark

sc = pyspark.SparkContext()
sqlContext = pyspark.SQLContext(sc)

# Création de la structure de nos données
from pyspark.sql.types import *

schema_ant = StructType([StructField("t", IntegerType()),
                     StructField("AntennaId", IntegerType()),
                     StructField("EventCode", IntegerType()),
                     StructField("PhoneId", IntegerType()),
                     StructField("x", FloatType()),
                     StructField("y", FloatType()),
                     StructField("TileId", IntegerType()) ])

# Instanciation d'un DataFrame vide
df_main = sqlContext.createDataFrame(sc.emptyRDD(), schema_ant)

# Fonction venant actualiser le df_main en se connectant au batch envoyés par le stream
def actualisation(base, batch):
    
    base = base.union(batch.na.drop() \
                           .orderBy('t', ascending=False) \
                           .dropDuplicates(subset = ['PhoneId']))
    
    base = base.orderBy('t', ascending=False) \
               .coalesce(1) \
               .dropDuplicates(subset = ['PhoneId'])
    
    return base


################ PARTIE STREAM ######################

# from pyspark.sql import SparkSession

# spark = SparkSession.builder \
#   .appName("Spark Structured Streaming from Kafka") \
#   .getOrCreate()

# sdfAntennes = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "localhost:9092") \
#   .option("subscribe", "antennes") \
#   .option("startingOffsets", "latest") \
#   .load() \
#   .selectExpr("CAST(value AS STRING)")

# def parse_data_from_kafka_message(sdf, schema):
#     from pyspark.sql.functions import split
#     assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
#     col = split(sdf['value'], ',')
#     for idx, field in enumerate(schema):
#         sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
#     sdf = sdf.select([field.name for field in schema])
#     return  sdf

# sdfAntennes = parse_data_from_kafka_message(sdfAntennes, schema_ant)

# sdfAntennes = sdfAntennes.select(['PhoneId', 'x', 'y']).writeStream.format("console").start().awaitTermination()

################ PARTIE Falsk ######################
from flask import Flask, request

app = Flask(__name__)

def create_plot(feature):

    N = 1000
    random_x = np.random.randn(N)
    random_y = np.random.randn(N)

    # Create a trace
    data = [go.Scatter(
        x = random_x,
        y = random_y,
        mode = 'markers'
    )]


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
 
    return graphJSON


@app.route("/")
def hello():

	from pyspark.sql import SparkSession
	
	spark = SparkSession.builder.appName("Spark Structured Streaming from Kafka").getOrCreate()
	sdfAntennes = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "antennes").option("startingOffsets", "latest").load().selectExpr("CAST(value AS STRING)")

	def parse_data_from_kafka_message(sdf, schema):
		from pyspark.sql.functions import split
		assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
		col = split(sdf['value'], ',')
		for idx, field in enumerate(schema):
			sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
		sdf = sdf.select([field.name for field in schema])
		return  sdf

	sdfAntennes = parse_data_from_kafka_message(sdfAntennes, schema_ant)

	return sdfAntennes.select(['PhoneId', 'x', 'y']).writeStream.format("console").start().awaitTermination()


if __name__ == "__main__":
    app.run(debug=True, port=2003)



















# query = sdfAntennes.writeStream.format("console").start()
# query = sdfAntennes.groupBy("AntennaId").count()
# query.writeStream.outputMode("complete").format("console").start().awaitTermination()
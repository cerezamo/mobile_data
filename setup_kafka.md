# **Simulation d'un Data Stream avec `Kakfa`**

### Création d'une variable d'environnement `Kakfa`

Ajouter la ligne suivante dans le fichier ~/.bashrc
```console
export KAFKA="/home/cesar/.local/kafka_2.12-2.2.0/"
```

## 1. **Démarage du zookeeper**

Pour démarrer le zookeeper en exécutant :
```console
$KAFKA/bin/zookeeper-server-start.sh -daemon $KAFKA/config/zookeeper.properties
```

Pour voir le status du zookeeper :
```console
echo stat | nc localhost 2181 | grep Mode
```

## 2. **Démarage du serveur `Kakfa`**

```console
$KAFKA/bin/kafka-server-start.sh -daemon $KAFKA/config/server.properties
```

```console
$KAFKA/bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids
```


## 3. **Création de topics**

Création :
```console
$KAFKA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic antennes
```

Suppression :
```console
$KAFKA/bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic antennes
```

Liste des topics :
```console
$KAFKA/bin/kafka-topics.sh --list --zookeeper localhost:2181
```

## 4. **Simulation du Stream**

Activation du stream :
```console
(cat /home/cesar/cours/ensae/donnees_distrib/projet/mobile_data/kafka_minimal_df.csv | split -l 10 --filter="$KAFKA/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic antennes; sleep 0.5" > /dev/null ) &
```

Affichage du stream dans la sortie de la console :
```console
$KAFKA/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic antennes --from-beginning
```

## 5. **Connexion de PySpark au Stream**

On commence par lancer PySpark avec une commande précisant l'import du package `spark-sql-kafka`
```console
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5
```

Dans un notebook `PySpark`
```python
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 pyspark-shell'

from pyspark.sql import SparkSession
```

## **Script Python**

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName("Spark Structured Streaming from Kafka") \
  .getOrCreate()

sdfRides = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "antennes") \
  .option("startingOffsets", "latest") \
  .load() \
  .selectExpr("CAST(value AS STRING)")

from pyspark.sql.types import *

schema_ant = StructType([StructField("t", IntegerType()),
                     StructField("AntennaId", IntegerType()),
                     StructField("EventCode", IntegerType()),
                     StructField("PhoneId", IntegerType()),
                     StructField("x", FloatType()),
                     StructField("y", FloatType()),
                     StructField("TileId", IntegerType()) ])

def parse_data_from_kafka_message(sdf, schema):
    from pyspark.sql.functions import split
    assert sdf.isStreaming == True, "DataFrame doesn't receive streaming data"
    col = split(sdf['value'], ',')
    for idx, field in enumerate(schema):
        sdf = sdf.withColumn(field.name, col.getItem(idx).cast(field.dataType))
    return sdf.select([field.name for field in schema])

sdfAntennes = parse_data_from_kafka_message(sdfRides, schema_ant)

query2 = sdfAntennes.writeStream.format("console").start()
```

## Fixe problème

Résinstaller kafka et modifier $KAFKA/config/server.configuration en décommentant la ligne `listeners=PLAINTEXT://:9092`


























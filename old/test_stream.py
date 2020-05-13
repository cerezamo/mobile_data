import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    sc = SparkContext(appName="Count lines")
    ssc = StreamingContext(sc, 2)

    brokers, topic = sys.argv[1:]
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic],{"metadata.broker.list": brokers})
    lines = directKafkaStream.map(lambda x: 1).reduce(lambda x, y: x + y)
    print("salut")
#    directKafkaStream.show()
    print("coucou")
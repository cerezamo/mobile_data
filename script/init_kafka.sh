$KAFKA/bin/zookeeper-server-start.sh -daemon $KAFKA/config/zookeeper.properties
$KAFKA/bin/kafka-server-start.sh -daemon $KAFKA/config/server.properties
$KAFKA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic antennes

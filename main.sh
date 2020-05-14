#!/bin/bash
echo "Suppression des anciens dossiers :\n- /tmp/zookeeper/\n- /tmp/kafka-logs/\n- $KAFKA/checkpoint ..."
sudo rm -rf /tmp/zookeeper/
sudo rm -rf /tmp/kafka-logs/
# A rajouter " si existe" ??  
sudo rm -rf $KAFKA/checkpoint	
echo "Suppression effectuée."

echo "Démarrage du zookeeper sur le port 2181..."
$KAFKA/bin/zookeeper-server-start.sh -daemon $KAFKA/config/zookeeper.properties
echo "Démarrage du zookeeper réussi."
echo "Mode de démarage du zookeeper :"
sleep 1
echo stat | nc localhost 2181 | grep Mode

echo "Démarrage du serveur Kafka sur le port 2181..."
$KAFKA/bin/kafka-server-start.sh -daemon $KAFKA/config/server.properties
sleep 3
echo "Démarrage du serveur Kafka réussi."
echo "ID du serveur Kafka :"
$KAFKA/bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids
#Rajouter 'verifier que c'est ok il y a quelque chose'

echo "Création des 2 topics Kafka antennesIntput et antennesOutput..."
$KAFKA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic antennesIntput
echo "antennesIntput : OK"
$KAFKA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic antennesOutput
echo "antennesOutput : OK"
echo "Instanciations réussites."
echo "Liste des topics Kafka créés :"
$KAFKA/bin/zookeeper-shell.sh localhost:2181 ls /brokers/topics

echo "L'environnement a été mis en place avec succès !"

echo "Exécution du script python consommant les données du topic antennesIntput, les retraitant, et les envoyant vers le topic antennesOutput..."
python app/producer_spark.py &
sleep 5
echo "Le topic antennesOutput est configuré et en attente de données."

echo "Production de données vers antennesIntput..."
(cat /home/cesar/cours/ensae/donnees_distrib/projet/mobile_data/kafka_ingestion.csv | split -l 500 --filter="$KAFKA/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic antennesInput; sleep 10" > /dev/null ) &
sleep 1
echo "Le topic antennesIntput produit désormais des données prêtes à être consommées par antennesOutput."

echo "Lancement de l'application web :"
python app/flask_app.py &

sleep 5
xdg-open http://127.0.0.1:2000/
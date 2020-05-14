#!/bin/bash

echo "==================="
echo "ETAPE 0 : PREREQUIS"
echo -e "===================\n"

read -p "Etes-vous bien placé dans le dossier source du projet ? [Y/N] : " check_folder
if [ "$check_folder" != "Y" ]; then
    echo "Relancez l'exécution du script depuis le dossier source du projet."
    exit 1
fi

read -p "Avez-vous bien activé l'environnement Python adéquat ? [Y/N] : " check_pyenv
if [ "$check_pyenv" != "Y" ]; then
    echo "Relancez le script après avoir activé votre environnement Python."
    exit 1
fi

read -p "Appuyez sur entrer pour continuer..."
echo -e "\n"

echo "================================="
echo "ETAPE 1 : INITIALISATION DE KAFKA"
echo -e "=================================\n"

sleep 0.5

if [ -d "/tmp/zookeeper/" ]; then
	echo "Suppression de l'ancien dossier /tmp/zookeeper/ ..."
	sudo rm -rf /tmp/zookeeper/
	echo "Suppression effectuée."
fi

sleep 0.5

if [ -d "/tmp/kafka-logs/" ]; then
	echo "Suppression de l'ancien dossier /tmp/kafka-logs/ ..."
	sudo rm -rf /tmp/kafka-logs/
	echo "Suppression effectuée."
fi

sleep 0.5

if [ -d "${KAFKA}checkpoint" ]; then
	echo "Suppression des anciens checkpoints situés dans le dossier ${KAFKA}checkpoint ..."
	sudo rm -rf $KAFKA/checkpoint	
	echo "Suppression effectuée."
fi

sleep 0.5

# echo "Suppression des anciens dossiers :\n- /tmp/zookeeper/\n- /tmp/kafka-logs/\n- $KAFKA/checkpoint ..."
# sudo rm -rf /tmp/zookeeper/
# sudo rm -rf /tmp/kafka-logs/
# # A rajouter " si existe" ??  
# sudo rm -rf $KAFKA/checkpoint	
# echo "Suppressions effectuées."

echo "Démarrage du zookeeper sur le port 2181..."
$KAFKA/bin/zookeeper-server-start.sh -daemon $KAFKA/config/zookeeper.properties
echo "Démarrage du zookeeper réussi."
echo "Mode de démarage du zookeeper :"
sleep 1
echo stat | nc localhost 2181 | grep Mode

echo -e "\nDémarrage du serveur Kafka sur le port 2181..."
$KAFKA/bin/kafka-server-start.sh -daemon $KAFKA/config/server.properties
sleep 3
echo "Démarrage du serveur Kafka réussi."
echo "ID du serveur Kafka :"
$KAFKA/bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids
#Rajouter 'verifier que c'est ok il y a quelque chose'

echo -e "\nCréation des 2 topics Kafka antennesIntput et antennesOutput..."
$KAFKA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic antennesIntput
echo "antennesIntput : OK"
$KAFKA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic antennesOutput
echo "antennesOutput : OK"
echo "Instanciations réussites."
echo "Liste des topics Kafka créés :"
$KAFKA/bin/zookeeper-shell.sh localhost:2181 ls /brokers/topics

echo -e "\nL'environnement a été mis en place avec succès !"
read -p "Appuyez sur entrer pour continuer..."
echo -e "\n"

echo "==============================="
echo "ETAPE 2 : EXECUTION DES SCRIPTS"
echo -e "===============================\n"

echo "Exécution du script python consommant les données du topic antennesIntput, les retraitant, et les envoyant vers le topic antennesOutput..."
python app/producer_spark.py &> logs/producer_spark.log &
sleep 5 
echo -e "La connexion entre les topics antennesIntput et antennesOutput est établie.\n"

echo "Production de données vers antennesIntput..."
(cat /home/cesar/cours/ensae/donnees_distrib/projet/mobile_data/kafka_ingestion.csv | split -l 30 --filter="$KAFKA/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic antennesInput; sleep 10" &> logs/antennesProducer.log ) &
sleep 1
echo -e "Le topic antennesIntput produit désormais des données prêtes à être consommées par antennesOutput.\n"

read -p "Appuyez sur entrer pour continuer..."
echo -e "\n"

echo "========================================"
echo "ETAPE 3 : DEMARRAGE DE L'APPLICATION WEB"
echo -e "========================================\n"

echo "Lancement de l'application web..."
python app/flask_app.py &> logs/flask_app.log &
sleep 5
echo "L'application web lancées à l'adresse http://127.0.0.1:2000/"
echo "BIG BROTHER IN DA HOOD !!"

sleep 1
xdg-open http://127.0.0.1:2000/



# sudo service mongodb start 
# Aller dans "mobile data"
# mongoimport --type csv -d mobiledata -c antennes --headerline kafka_ingestion.csv
# Aller dans moobiledata/app/templates/static/
# mongoimport -d mobiledata -c fond --headerline antennes.json --JsonArray
# python flaks_app_mongodb2.py
#


echo "Mise en place du produceur du topic antennesInput ..."
(cat /home/cesar/cours/ensae/donnees_distrib/projet/mobile_data/kafka_ingestion.csv | split -l 30 --filter="$KAFKA/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic antennesInput; sleep 10" > /dev/null ) &
sleep 10
echo "OK\n\n"

#La faut mettre une adresse générale + en amont il faut créer la variable $KAFKA 

echo "Lancement du traitement PySpark et mise en place du produceur du topic antennesOutput ..."
python ../app/producer_many_sparktest_2.py &
sleep 10
echo "OK\n\n"

echo "Affichage du consumer du topic antennesOutput ..."
$KAFKA/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic antennesOutput --from-beginning
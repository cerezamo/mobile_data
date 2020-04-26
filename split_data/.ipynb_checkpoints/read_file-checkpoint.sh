for i in /home/cesar/cours/ensae/donnees_distrib/projet/mobile_data/split_data/split/*/*; do 
	echo $i;
	(cat $i | split -l 100000 --filter="~/.local/kafka_2.12-2.2.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic antennes; sleep 1" > /dev/null ) &
	sleep 1;
done
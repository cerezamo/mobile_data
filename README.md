# Traitement de données distribuées - ENSAE 2020

* **César Roaldès**  - [Github](https://github.com/CesarRoaldes)
* **Morgane Hoffmann**  - [Github](https://github.com/cerezamo)


Ce projet est réalisé dans le cadre du cours Traitement de données distribuées enseigné par Antoine Ly et développé sous l'OS Ubuntu 18.04 LTS.

## Introduction 

Le projet a pour but de répliquer un pipeline de données mobiles en temps réels. L'architecture construite est représentée dans la figure ... . 


## Getting Started - Prérequis

Nous supposons que Python, Spark ainsi qu'un environnement Pyspark sont installés sur votre ordinateur. Si ce n'est pas le cas veuillez vous référer aux instruction (cf github antoine)

### Simulateur

#### Installation
Si vous voulez être en mesure de faire vous mêmes vos propres simulations, suivez ce premier chapitre. Sinon, il vous suffit de cloner notre repo et d'utiliser les fichiers que nous avons simulé, dans ce cas passez au chapitre suivant. 

Avant toute chose, il faudra s'assurer d'installer la bibliothèque GEOS C++, elle peut être télécharger à l'adresse suivante :  https://trac.osgeo.org/geos (ATTENTION seule la version 3.7.1 est compatible !! )

Déployez la avec le code suivant : 

```
$ ./configure
$ make
$ make install
```
L'installation peut prendre quelques minutes. 


Pour installer le simulateur, télécharger le code source de la repository github : https://github.com/bogdanoancea/simulator 

```
$git clone https://github.com/bogdanoancea/simulator.git
```

Lorsque le répertoire est téléchargé, ouvrez le fichier *makefile.inc* avec l'éditeur de texte de votre choix et modifiez les variables PROJ_HOME et GEOS_HOME. PROJ_HOME doit pointer sur le fichier où vous avez téléchargé le code source du micro-simulateur alors que GEOS_HOME doit pointer sur le fichier du code source de GEOS. Dans notre implémentation nous avons par exemple : 


```
PROJ_HOME = /home/user/simulator
GEOS_HOME = /home/user/geos-3.7.1
```

Avant de passer à l'installation du simulateur, assurez-vous de copier le fichier geos-3.7.1/src/.libs/libgeos.a dans le dossier racine de GEOS. Pour celà, placer vous dans le dossier racine geos-3.7.1/ puis exécuter la commande :

```
cp ./src/.libs/libgeos.a ./libgeos.a
```

Revenir dans le dossier racine du simulateur simulator/ et procéder à l'installation avec les commandes :

```
make 
make install
```

Le simulateur est installé ! 

**Ces instructions sont valables pour Ubuntu 18.04 LTS, pour plus d'informations sur l'installation du simulateur sur les diofférents OS, veuillez vous référer aux instructions de https://github.com/bogdanoancea/simulator**

#### Simuler des données avec le micro-simulateur 

Avant de simuler les données allez regarder les inputs possibles (nombre d'antennes, d'individus, map,...etc), les fichiers inputs se trouvent dans data/ (Notre simulation utilise la dataset2 ou simulation Madrid). Lorsque vous avez choisis l'ensemble de vos paramètres et avez modifié en conséquences les fichiers inputs ouvrez votre terminal, allez dans le fichier 'simulateur' et tapez le code suivant (Bien entendu si vous choisissez la dataset 1, ce code est sujet à modifications) : 

```
$Release/simulator -m ./data/dataset2/mapMadrid.wkt -s ./data/dataset2/simulation.xml -a ./data/dataset1/antennasMadrid.xml -p ./data/dataset2/persons.xml -pb ./data/dataset1/probabilities.xml -v -o
```

Les fichiers ont été simulé !


#### Préparation des données 

Certains retraitements ont été effectué afin de simuler des envois des antennes vers Kafka et afficher des cartes sur l'application Flask. Les 









La suite des instructions est à présent obligatoire pour être en mesure de faire tourner le code. 

### Kafka

Le code ci dessous permettra d'installer Kafka, dans le fichier que vous souhaitez : 

```

#Kafka 2.2.0 installation
curl https://www-us.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz -o kafka_2.12-2.2.0.tgz
tar xzf kafka_2.12-2.2.0.tgz
ln -sf kafka_2.12-2.2.0 kafka

```


## Running 











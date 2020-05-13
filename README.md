# Traitement de données distribuées - ENSAE 2020

* **César Roaldès**  - [Github](https://github.com/RoaldesCesar)
* **Morgane Hoffmann**  - [Github](https://github.com/cerezamo)


Ce projet est réalisé dans le cadre du cours Traitement de données distribuées enseigné par Antoine Ly. 

## Introduction 

Ce projet a pour but de répliquer un pipeline de données mobiles en temps réels. L'architecture construite est représentée dans la figure ... . 


## Getting Started
### Prerequis

#### Simulateur
Si voulez être en mesure de faire vous mêmes vos propres simulations, suivez ce premier chapitre. Sinon, il vous suffit de cloner notre repo et d'utiliser les fichiers que nous avons simulé, dans ce cas passez au chapitre suivant. 

Avant toute chose, il faudra s'assurer d'installer la bibliothèque GEOS C++, elle peut être télécharger à l'adresse suivante :  https://trac.osgeo.org/geos (ATTENTION seule la version 3.7.1 est compatible !! )

Déployez la avec le code suivant : 

```
$ ./configure
$ make
$ make install
```
L'installation peut prendre quelques minutes. 


Pour installer le simulateur, télécharger le code source de la reposotory github : https://github.com/bogdanoancea/simulator 

```
$git clone https://github.com/bogdanoancea/simulator.git
```

Lorsque le simulateur est installé, ouvrez le fichier *makefile.inc* avec l'éditeur de texte de votre choix et modifiez les variables PROJ_HOME et GEOS_HOME. PROJ_HOME doit pointé sur le fichier où vous avez téléchargé le code source du micro-simulateur alors que GEOS_HOME doit pointer sur le fichier du code source de GEOS. Dans notre implémentation nous avons par exemple : 

PROJ_HOME = /home/user/simulator

GEOS_HOME = /home/user/geos-3.7.1


Le simulateur est installé ! 

### Spark ? 

### Kafka

Le code ci dessous permettra d'installer Kafka : 

```

#Kafka 2.2.0 installation
curl https://www-us.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz -o kafka_2.12-2.2.0.tgz
tar xzf kafka_2.12-2.2.0.tgz
ln -sf kafka_2.12-2.2.0 kafka

```


## Running 











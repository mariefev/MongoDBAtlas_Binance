# Load_Atlas_Readme.md

Ce Readme a pour objectif de donner les informations nécessaires à la création et au chargement d'une base de données MongoDB Atlas sur le Cloud portant les informations historiques (klines) de tous les marchés (BTCEUR, BTCUSDT, ...) correspondant à la cryptomonnaie Bitcoin (BTC) sur un intervalle de temps défini (intervalle du jour choisi dans cette partie du projet, mais jour, heure, minute ou seconde possible).

Ce projet a été réalisé dans le cadre du projet fil rouge "CryptoBot sur Binance" de la formation en bootcamp Data Engineer dispensée par DatascienTest. Vous pouvez remplacer les informations de la Virtual Machine Airflow (VM sur Ubuntu) offerte par Datascientest par les informations de votre machine.

Vous pourrez réaliser des dashboards des données historiques des marchés BTC* en suivant les 4 étapes suivantes :


# 1) Création du cluster sur MongoDB Atlas sur le Cloud

Création d'un compte sur MongoDB Atlas
https://account.mongodb.com/account/login?signedOut=true
Renseigner la première page de renseignement sur le projet

Création d'un projet "project 0" dont vous etes le owner
avec éventuellement des ajouts de membres au projet "project 0"
Création d'un déploiement avec un cluster "Cluster1" de fournisseur AWS de région Paris (exemple pour les utilisateurs proches de Paris) de type M0 FREE qui octroie 512 MB de mémoire RAM Shared et de vCPU Shared

### Très important : sélectionner le type M0 FREE !

NB : le tag est obligatoire : vous pouvez renseigner application  : Binance
cliquer sur create 

### Renseigner les paramètres sécurité dans la page Security Quickstart

Le username de connexion est pré-rempli
Renseigner le password dans le cas d'une authentification par mot de passe

Renseigner la liste des adresses IP autorisées à accéder le cluster1 du projet project1 avec l'adresse IP de la VM de DataScientest de la session de connexion en cours
(vous pouvez aussi ne pas restreindre les adresses IP autorisées, ce qui n'est pas conseillé)

valider la page : Finish and close

### Renseigner les autres users (facultatif)
Dans ce cas il faut renseigner d'abord des rôles personnalisés :
readonly ou read and write sur la collection, la base ou projet, ou bien administrateur (déconseillé, car l'owner l'est déjà)


### Votre cluster "Cluster1" est prêt a être chargé.

# 2) Préparation de l'environnement

Sur la Virtual Machine de Datascientest (ou sur votre machine)
création d'un fichier .env 
touch .env
pour contenir :
-les paramètres de connexion à MongoDB Atlas
ATLAS_USER = "XXX"
ATLAS_PWD = "XXX"
XXX correspond au user paramétré sur MongoDB Atlas (owner ou autres membres du projet).

-les clés de connexion à Binance ne sont pas nécessaires pour cette partie du projet 
BINANCE_API=XXXX
BINANCE_SECRET=XXX

Création d'un répertoire results
mkdir results

# 3) Lancement du chargement de la Base de Données Atlas sur le Cloud

### Test de connexion à la base
python3 Test_ping_MongoDBAtlas.py

### Chargement de la base
python3 historical-data-engine_Atlasv4.py > results/load_engine_Atlasv4.txt

# 4) Création des dashboards sur MongoDB Atlas

Atlas permet de réaliser rapidement des charts, pour certains très adaptés aux klines (charts de type Candlesticks)

### Vérification de l'état de la base
vous pouvez consulter l'espace mémoire utilisé en sélectionnant : Project1/Overview/Deployment/database : la BD "Binance_historical_All_BTC" est là.
vous pouvez consulter un exemple de données de la collection sur le menu "Browse collections" : la collection "BTC_markets" est là.

### Création du dashboard
- Création du dashboard du projet "Project1" en sélectionnant Project1/Overview/Deployment/database/Browse collections/ visualize your data 
ou en sélectionnant Project1/Chart/Add Dashboard ou en sélectionnant un dashboard existant : Project1/Chart/Dashboard existant
- Création d'un graphique : en sélectionnant Add Chart
- Sélectionner votre source de données : cluster1 / Binance_hsitorical_All_BTC / BTC_markets
- Sélectionner votre type de chart :
    exemple candlesticks (champs Y : Close, Open, High, Low prédéfinis et date en X) 
    exemple discreteline (champs Close en Y, date en X, market en series)

# Bonus : Consultation des dashboards (facultatif)
vous pouvez donner accès en lecture des dashboards aux autres utilisateurs de votre BD Atlas que vous aurez paramétrés préalablement avec un rôle en lecture.
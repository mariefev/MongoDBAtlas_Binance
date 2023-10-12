# MongoDBAtlas_Binance
Historical data of BTC* markets  from Binance loading on MongoDB Atlas database on Cloud

# Load_Atlas_Readme.md

This Readme aims to provide the information necessary for the creation and loading of a MongoDB Atlas database on the Cloud containing the historical information (klines) of all markets (BTCEUR, BTCUSDT, etc.) corresponding to the cryptocurrency Bitcoin (BTC) over a defined time interval (interval of the day chosen in this part of the project, but day, hour, minute or second possible).

This project was carried out as part of the “CryptoBot on Binance” common thread project of the Data Engineer bootcamp training provided by DataScientest. You can replace the information from the Virtual Machine Airflow (VM on Ubuntu) offered by DataScientest with the information from your machine.

You will be able to create dashboards of historical BTC* market data by following the following 4 steps:


# 1) Creating the cluster on MongoDB Atlas on the Cloud

Creating an account on MongoDB Atlas
https://account.mongodb.com/account/login?signedOut=true
Complete the first information page on the project

Creation of a project "project1" of which you are the owner
with possibly additions of members to the project "project1"
Creation of a deployment with a "Cluster1" cluster from AWS provider in the Paris region (example for users near Paris) of type M0 FREE which grants 512 MB of Shared RAM memory and Shared vCPU

### Very important: select the M0 FREE type!

NB: the tag is mandatory: you can enter application: Binance
click on create

### Complete the security parameters in the Security Quickstart page

The login username is pre-filled
Enter the password in the case of password authentication

Complete the list of IP addresses authorized to access cluster1 of the project project1 with the IP address of the DataScientest VM of the current connection session
(you can also not restrict the allowed IP addresses, which is not recommended)

validate the page: Finish and close

### Enter other reader users (optional)
In this case you must first enter personalized roles:
readonly or read and write on the collection, database or project, or administrator (not recommended, because the owner already is)


### Your cluster "Cluster1" is ready to be loaded.

# 2) Preparing the environment

On the DataScientest Virtual Machine (or on your machine)
creating an .env file
touch .env
to contain:
-MongoDB Atlas connection parameters
ATLAS_USER = "XXX"
ATLAS_PWD = "XXX"
XXX corresponds to the user configured on MongoDB Atlas (owner or other members of the project).

-Binance login keys are not necessary for this part of the project
BINANCE_API=XXXX
BINANCE_SECRET=XXX

Creating a results directory
mkdir results

# 3) Start loading the Atlas Database on the Cloud

### Base connection test
python3 Test_ping_MongoDBAtlas.py

### Loading the database
python3 historical-data-engine_Atlasv4.py > results/load_engine_Atlasv4.txt

# 4) Creation of dashboards on MongoDB Atlas

Atlas allows you to quickly create charts, some of which are very suitable for klines (Candlesticks type charts)

### Checking the status of the database
you can consult the memory space used by selecting: Project1/Overview/Deployment/database: the “Binance_historical_All_BTC” database is there.
you can consult an example of data from the collection on the “Browse collections” menu: the “BTC_markets” collection is there.

### Creation of the dashboard
- Creation of the project dashboard "Project1" by selecting Project1/Overview/Deployment/database/Browse collections/visualize your data
or by selecting Project1/Chart/Add Dashboard or by selecting an existing dashboard: Project1/Chart/Existing Dashboard
- Creating a chart: by selecting Add Chart
- Select your data source: cluster1 / Binance_hsitorical_All_BTC / BTC_markets
- Select your chart type:
     Candlestick example (Y fields: Close, Open, High, Low predefined and date in X)
     Discrete Line example (Close fields in Y, date in X, market in series)

# Bonus: Consultation of dashboards (optional)
you can give reading access to the dashboards to other users of your Atlas BD that you have previously configured with a reading role.

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os

load_dotenv()
user=os.getenv("ATLAS_USER")
pwd=os.getenv("ATLAS_PWD")
#print(user, pwd)
clustername="Cluster1"
uri = "mongodb+srv://{0}:{1}@{2}.sgf90rd.mongodb.net/?retryWrites=true&w=majority".format(user, pwd, clustername)
print("tentative de connexion user, pwd, clustername")
print("uri", uri)
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# Close Mongo
client.close()


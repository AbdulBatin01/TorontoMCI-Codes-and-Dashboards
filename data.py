import pandas as pd
import pymongo
from pymongo import MongoClient
import requests

uri = "mongodb+srv://Abdul-Batin:abdul2001@cluster0.eeswfug.mongodb.net/?retryWrites=true&w=majority"
client =MongoClient(uri)
db = client.get_database('Major_Crime_Indicators')
records = db['AllData']

raw_data = records.find()

pd_Data = pd.DataFrame(raw_data)
pd_Data.drop(["_id"], axis=1, inplace=True)

MCI_by_Occurence = pd_Data.groupby(['MCI'])['MCI'].count().reset_index(name='Occurence')

hood_by_MCI_Count = pd_Data.groupby(['Neighbourhood','MCI','premises_type'])['MCI'].count().sort_values(ascending = False).reset_index(name='Occurence')





#print(pd_Data)
# Script to create database from scratch

import pymongo
import json
from pymongo import MongoClient, InsertOne
import os, glob

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="Path to JSON files", default = './data')
parser.add_argument("--dbname", help="DB name", default = 'jsonDB')
parser.add_argument("--target", help="ECOND or ECONT", default = 'ECOND')
args = parser.parse_args()

# utility scripts

from json_uploader import jsonFileUploader



client = pymongo.MongoClient("mongodb://127.0.0.1:27017") # Connect to local database

client.drop_database(args.dbname)

mydatabase = client[args.dbname] # create new database
mycol = mydatabase[args.target] # dict of type {'unique_id' : json_full_report}

fnames = glob.glob(args.path + '/' + '*.json')
print("Will add the files located in %s (total %d)"%(args.path,len(fnames)))

for fname in fnames:
    print(fname)
    jsonFileUploader(fname,mycol)



#jsonObj = json.load(open("%s/data/report_ECOND_2024-04-17_21-49-01.json"%path,'r'))
   
#x = mycol.insert_one(jsonObj) # Write in DB

# Print written object

#for obj in mydatabase['hex46'].find():
#    print(obj)
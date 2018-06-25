from pymongo import MongoClient

def connect(dbname, host='localhost', port=27017):
    """:return mongo database"""
    client = MongoClient(host, port)
    db = client[dbname]
    return db



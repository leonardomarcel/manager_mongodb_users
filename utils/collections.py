import pymongo
import os

class MongoClient:
    MONGO_URI = os.environ['MONGO_URI']
    def __init__(self, bd_name, collection_name):
        self.client = pymongo.MongoClient(self.MONGO_URI)
        self.db = self.client[bd_name]  # Nome do banco de dados
        self.collection = self.db[collection_name]  # Nome da coleção
    def get_collection(self):
        return self.collection
import pymongo
from bson import ObjectId

class MongoClient:
    def __init__(self, bd_name, collection_name):
        self.client = pymongo.MongoClient("mongodb://200.100.50.50:27017/")
        self.db = self.client[bd_name]  # Nome do banco de dados
        self.collection = self.db[collection_name]  # Nome da coleção
    def get_collection(self):
        return self.collection
    

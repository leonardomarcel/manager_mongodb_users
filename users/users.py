from utils.collections import MongoClient
from bson import ObjectId

client = MongoClient("users", "users")
def list_users():
    users = list(client.get_collection().find())
    for user in users:
        user["_id"] = str(user["_id"])  # Converter ObjectId para string
    return users

def add_user(user):
    return client.get_collection().insert_one(user)

def update_user(user_id, user):
    return client.get_collection().update_one({"_id": ObjectId(user_id)}, {"$set": user})

def delete_user(user_id):
    return client.get_collection().delete_one({"_id": ObjectId(user_id)})

def get_user_by_id(user_id):
    return client.get_collection().find_one({"_id": ObjectId(user_id)})

def get_user_by_username(username):
    return client.get_collection().find_one({"username": username})
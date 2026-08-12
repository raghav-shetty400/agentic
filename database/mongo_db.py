from pymongo import MongoClient

MONGO_URI = "YOUR_MONGODB_CONNECTION_STRING"

client = MongoClient(MONGO_URI)

db = client["RideEase-app"]

users_collection = db["users"]
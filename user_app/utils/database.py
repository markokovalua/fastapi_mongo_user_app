from os import environ
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = environ.get("MONGO_URI")
MONGO_DB_CLUSTER = environ.get("MONGO_DB_CLUSTER")
COLLECTION_DB = environ.get("COLLECTION_DB")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_CLUSTER]
user_collection = db[COLLECTION_DB]
# create index for email to keep unique emails, it restricts non-admin user
# to modify/delete others users data afterward access token generation
# (if there are same auth credentials of several users,
# it is possible to get access to not your user data - so to avoid it is used such a way)
user_collection.create_index([("email", pymongo.ASCENDING)], unique=True)
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

_client = MongoClient(os.getenv("MONGO_URI"))
_db = _client[os.getenv("MONGO_DB")]


def db():
    return _db


def users_col():
    return _db["users"]


def create_indexes():
    users_col().create_index("email", unique=True)

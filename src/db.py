from pymongo import MongoClient

from .config import settings


def get_db():
    client = MongoClient(settings.MONGODB_URL)
    return client.test_first_vds

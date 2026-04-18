from pymongo import MongoClient
from core.config import settings

class Database:
    client: MongoClient = None

    def connect(self):
        self.client = MongoClient(settings.MONGO_URI)
        print(f"Connected to MongoDB at {settings.MONGO_URI}")

    def get_db(self):
        return self.client[settings.DATABASE_NAME]

    def close(self):
        if self.client:
            self.client.close()

db = Database()

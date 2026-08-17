from pymongo import MongoClient
from app.config.settings import Settings

creds = Settings()
Monog_URI = creds.mongo_url
client = MongoClient(Monog_URI)

db = client['pm_database']

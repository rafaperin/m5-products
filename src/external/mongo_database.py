from pymongo import mongo_client, ASCENDING
from src.config.config import settings

DB_USER = settings.db.MONGO_USERNAME
DB_PASS = settings.db.MONGO_PASSWORD
DB_HOST = settings.db.MONGO_HOST
DB_NAME = settings.db.MONGO_DATABASE
MONGO_DB_URL = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?authSource=admin"

client = mongo_client.MongoClient(MONGO_DB_URL)

db = client[settings.db.MONGO_DATABASE]
Product = db.products
Product.create_index([("product_id", ASCENDING)], unique=True)

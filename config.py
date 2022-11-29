import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

from pymongo import MongoClient

db_admin = os.environ.get("MONGO_USERNAME", "")
db_pass = os.environ.get("MONGO_PASSWORD", "")
db_url = f'mongodb://{db_admin}:{db_pass}@localhost:27017/?authSource=admin'
client = MongoClient(db_url)

db = client['bet']
collection = db["nba"]

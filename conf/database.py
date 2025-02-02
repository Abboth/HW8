import configparser
import os

from pathlib import Path
from mongoengine import connect
from pymongo import MongoClient
from pymongo.server_api import ServerApi


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = os.path.join(BASE_DIR, 'conf', 'config.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DATABASE_CONFIG = config["DB"]
MONGOENGINE_CONFIG = config["ME"]

mongo_user = DATABASE_CONFIG["USER"]
mongo_password = DATABASE_CONFIG["PWD"]
mongo_db = DATABASE_CONFIG["DB_NAME"]
mongo_domain = DATABASE_CONFIG["DOMAIN"]

client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_domain}"
                     f"/?retryWrites=true&w=majority", server_api=ServerApi('1'))

engine_user = MONGOENGINE_CONFIG["USER"]
engine_password = MONGOENGINE_CONFIG["PWD"]
engine_db = MONGOENGINE_CONFIG["DB_NAME"]
engine_domain = MONGOENGINE_CONFIG["DOMAIN"]
connect(
    db=engine_db,
    username=engine_user,
    password=engine_password,
    host=f"mongodb+srv://{engine_user}:{engine_password}@{engine_domain}"
         f"/{engine_db}?retryWrites=true&w=majority",
    alias="default"
)

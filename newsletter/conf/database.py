import configparser

from mongoengine import connect
from pymongo import MongoClient
from pymongo.server_api import ServerApi

config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get("DB", "USER")
mongo_password = config.get("DB", "PWD")
mongo_db = config.get("DB", "DB_NAME")
mongo_domain = config.get("DB", "DOMAIN")

client = MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_domain}"
                     f"/?retryWrites=true&w=majority", server_api=ServerApi('1'))

engine_user = config.get("ME", "USER")
engine_password = config.get("ME", "PWD")
engine_db = config.get("ME", "DB_NAME")
engine_domain = config.get("ME", "DOMAIN")
connect(
    db=engine_db,
    username=engine_user,
    password=engine_password,
    host=f"mongodb+srv://{engine_user}:{engine_password}@{engine_domain}"
         f"/{engine_db}?retryWrites=true&w=majority",
    alias="default"
)

import json
import logging
import redis

from conf.database import client, connect
from redis_lru import RedisLRU
from pymongo import errors

redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)

db = client["quotes"]

@cache
def find_in_documents(col: str, obj: dict):
    """Searching for data in database documents
    with using regex matching"""
    try:
        object_key = list(obj.keys())[0]
        value = obj[object_key]
        match col:
            case:
                fetched_data = db[col].find({object_key: {"$regex": value, "$options": "i"}})
                answer = ""
                for doc in fetched_data:
                    doc_keys = doc.keys()
                    for key in doc_keys:
                        answer += f"{key}: {doc.get(key)}\n"
                logging.info("Fetching data successfully") if answer else None
                result = json.dumps(answer)
                return result
    except errors.PyMongoError as err:
        logging.error(f"Error while searching for data{err}")


if __name__ == "__main__":
    find_in_documents("quotes", {"name": "albert"})

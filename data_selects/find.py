import logging
import redis
import json

from conf.quotes_database import client, connect
from redis_lru import RedisLRU
from pymongo import errors

redis_client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(redis_client)

db = client["quotes"]
quote_constructor = {"name": "author", "tag": "tags", "tags": "tags"}
author_constructor = {"person": "name", "description": "description"}


@cache
def find_in_documents(col: str, obj: str):
    """Searching for data in database documents
    with using regex matching
    and send to formatting"""

    try:
        list_data = obj.split(" ")
        dict_data = {list_data[0]: list_data[1]}
        object_key = list(dict_data.keys())[0]
        value = dict_data[object_key]
        key = quote_constructor[object_key] if object_key in quote_constructor \
            else author_constructor[object_key]
        fetched_data = None
        match key:
            case "author" | "tag" | "tags":
                fetched_data = db[col].find(
                    {key: {"$regex": value, "$options": "i"}}
                    if key in ["author", "tag"]
                    else {"$or": [{key: {"$regex": value[0], "$options": "i"}},
                                  {key: {"$regex": value[1]}, "$options": "i"}]}
                )
            case "name" | "description":
                fetched_data = db[col].find({key: {"$regex": value, "$options": "i"}})
        return formatting_data(col, fetched_data)
    except errors.PyMongoError as err:
        logging.error(f"Error while searching for data{err}")


def formatting_data(col: str, document: dict) -> bytes:
    """formatting documents to list[data]
    returning bytes list[data] format """

    result = []
    for doc in document:
        del doc["_id"]
        if col == "quote":
            doc["author"] = {"fullname": doc["author"]}
        else:
            doc["name"] = {"name": doc["name"]}
        result.append(doc)
    logging.info("Fetching data successfully") if result \
        else logging.info("Doesn't find any result for this request")

    return json.dumps(result).encode("utf-8")

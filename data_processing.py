import logging
import json

from conf.quotes_database import client, connect
from models.models import Author, Quote
from pymongo import errors
from pathlib import Path

db = client["quotes"]
logging.basicConfig(level=logging.INFO)


def get_data_from_json(json_file: Path):
    """getting data from json file
    and transmit to processing"""
    with open(json_file, "r", encoding="utf8") as file:
        try:
            data = json.load(file)
            name = json_file.stem
            json_data_processing(name, data)
        except FileNotFoundError as err:
            logging.error(f"Error with opening file {json_file}, file not found: {err}")


def json_data_processing(file_name: str, data_from_json: dict):
    """processing data from json file
    take dict to upload to Mongo"""
    try:
        if not isinstance(data_from_json, (dict, list)):
            raise TypeError("Data must be dict or list of dicts")
        name = file_name.replace(" ", "_")
        insert_data_to_mongo(name, data_from_json)
    except TypeError as err:
        logging.error(f"Error with processing of data {file_name}, data should to contain format key: value: {err}")


def insert_data_to_mongo(collection_name: str, data: dict) -> None:
    """Creating collection if needed and
    inserting processed data
    from get_data_from_json into Mongo"""
    try:
        match collection_name:
            case "authors":
                for author_data in data:
                    author = Author(
                        name=author_data["fullname"],
                        born_date=author_data["born_date"],
                        born_location=author_data["born_location"],
                        description=author_data["description"]
                    )
                    author.save()
                    logging.info(f"Author {author_data['fullname']} added to collection authors")
            case "quotes":
                for quote_data in data:
                    quote = Quote(
                        tags=quote_data["tags"],
                        author=quote_data["author"],
                        quote=quote_data["quote"],
                    )
                    quote.save()
                    logging.info(f"Quote of {quote_data['author']} added to collection quotes")
            case _:
                for record in data:
                    collection = db[collection_name]
                    collection.insert_one(record)
                    logging.info(f"Data added to collection {collection_name}")

    except errors.PyMongoError as err:
        logging.error(f"Error with inserting data to Mongo, {err}")


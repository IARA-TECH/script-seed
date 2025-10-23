from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from termcolor import colored
import random
from faker import Faker
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker("pt_BR")

class MongoStatements:
    def __init__(self, mongo_url=os.getenv('MONGO_URL'), db_name="iara"):
        client = MongoClient(mongo_url)
        self.__client = client
        db = client[db_name]
        self.__shifts = db["shifts"]
        self.__abacuses = db["abacuses"]
        self.__abacus_photos = db["abacus_photos"]
        self.__sheets = db["sheets"]

    def create_shift(self, name: str, starts_at: str, ends_at: str) -> dict:
        shift = {
            "name": name,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "created_at": datetime.now(),
        }
        result = self.__shifts.insert_one(shift)
        return self.__shifts.find_one({"_id": result.inserted_id})
    
    def create_abacus(self, factory_id: int, name: str, description: str, lines: list, columns: list) -> int:
        abacus = {
            "factory_id": factory_id,
            "name": name,
            "description": description,
            "lines": lines,
            "columns": columns
        }
        result = self.__abacuses.insert_one(abacus)
        return result.inserted_id

    def create_abacus_photo(self, factory_id: int, shift_id: ObjectId, abacus_id: ObjectId, lines:list, columns: list, taken_by: str, taken_at: datetime, url_blob:str, validated_by:str, values:list, shift_name:str, shift_starts_at:datetime, shift_ends_at:datetime) -> int:
        photo = {
            "factory_id": factory_id,
            "shift": {
                "_id": shift_id,
                "name": shift_name,
                "starts_at": shift_starts_at,
                "ends_at": shift_ends_at,
            },
            "abacus_id": abacus_id,
            "taken_by": taken_by,
            "taken_at": taken_at,
            "url_blob": url_blob,
            "validated_by": validated_by,
            "lines": lines,
            "columns": columns,
            "values": values
        }
        result = self.__abacus_photos.insert_one(photo)
        return result.inserted_id

    def create_sheet(self, factory_id: int, shift_id: ObjectId, abacus_photos_ids: list, date: datetime, shift_name:str, shift_starts_at:datetime, shift_ends_at:datetime):
        sheet = {
            "factory_id": factory_id,
            "shift_id": {
                "_id": shift_id,
                "name": shift_name,
                "starts_at": shift_starts_at,
                "ends_at": shift_ends_at,
            },
            "date": date,
            "abacus_photos": abacus_photos_ids
        }
        result = self.__sheets.insert_one(sheet)
        return result.inserted_id

    def close_connection(self):
        self.__client.close()
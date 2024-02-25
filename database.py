

import motor.motor_asyncio
from bson.objectid import ObjectId
import datetime

import json
from bson import json_util

class db:
    def __init__(self, uri:str, database_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[f'{database_name}']
        self.collection = self.db['users']

    async def create_user(self, user_id, name, referal, date_actives):
        user = await self.collection.find_one({'id': user_id})
        if not user:
            user_data = {
                'id': user_id,
                'name': name,
                'balance': 50,
                'referal': referal,
                'date_actives': date_actives
            }
            await self.collection.insert_one(user_data)
            if referal:
                return True
            return "noref"
        else:
            print("already in system")
            return False

    async def add_balance(self, user_id, amount):
        user = await self.collection.find_one({'id': user_id})
        if user:
            new_balance = user['balance'] + amount
            await self.collection.update_one({'id': user_id}, {'$set': {'balance': new_balance}})
            return True
        return False
    
    async def del_balance(self, user_id, amount):
        user = await self.collection.find_one({'id': user_id})
        if user:
            new_balance = user['balance'] - amount
            await self.collection.update_one({'id': user_id}, {'$set': {'balance': new_balance}})
            return True
        return False

    async def get_user_by_id(self, user_id):
        return await self.collection.find_one({'id': user_id})
    
    async def count_users(self):
        count = await self.collection.count_documents({})
        return count

    async def count_users_with_referral(self):
        count = await self.collection.count_documents({'referal': {'$ne': None}})
        return count
    async def get_all_users(self):
        cursor = self.collection.find({}, {'_id': 0, 'id': 1})
        user_ids = [user['id'] async for user in cursor]
        return user_ids

class InstagramDB:
    def __init__(self, uri: str, database_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db['instagram_links']

    async def create_entry(self, id, url):
        document = {"_id": id, "url": url}
        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def find_by_id(self, id):
        result = await self.collection.find_one({"_id": id})
        return result

    async def get_all_entries(self):
        documents = []
        cursor = self.collection.find({})
        for document in await cursor.to_list(length=None):
            documents.append(document)
        return json.loads(json_util.dumps(documents))
    

class TelegramDB:
    def __init__(self, uri: str, database_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db['telegram_data']

    async def create_entry(self, telegram_id, group_id, url):
        document = {
            "_id": telegram_id,
            "group_id": group_id,
            "url": url
        }
        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def find_by_id(self, telegram_id):
        result = await self.collection.find_one({"_id": telegram_id})
        return result

    async def get_all_entries(self):
        documents = []
        cursor = self.collection.find({})
        for document in await cursor.to_list(length=None):
            documents.append(document)
        return json.loads(json_util.dumps(documents))


class UserCollections:
    def __init__(self, uri: str, database_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
    
    async def create_entry(self, user_id: int, platform_id: int, platform_type: str):
        collection_name = f'user_{user_id}_data'
        collection = self.db[collection_name]
        document = {
            "type": platform_type,
            "id": platform_id,
            "user_id": user_id
        }
        result = await collection.insert_one(document)
        return result.inserted_id
    
    async def get_entries_by_user(self, user_id: int):
        collection_name = f'user_{user_id}_data'
        collection = self.db[collection_name]
        cursor = collection.find({"user_id": user_id})
        documents = await cursor.to_list(length=None)
        return documents
    
    async def find_by_platform_id(self, user_id: int, platform_id: int):
        collection_name = f'user_{user_id}_data'
        collection = self.db[collection_name]
        result = await collection.find_one({"id": platform_id})
        return result
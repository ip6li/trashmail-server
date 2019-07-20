from pymongo import MongoClient
from pymongo import errors
from config import Config
from logger import Logger


class Mongo:

    def __init__(self):
        self.__client = MongoClient(host=Config.getMongoURL(), socketTimeoutMS=10000)
        self.__db = self.__client[Config.getDB()]

    def insert(self, data):
        from pymongo.errors import ServerSelectionTimeoutError
        try:
            posts = self.__db.posts
            post_id = posts.insert_one(data).inserted_id
            return post_id
        except ServerSelectionTimeoutError as err:
            Logger.warn("Cannot connect to MongoDB server: " + str(err))
            raise err
        except errors as err:
            Logger.warn("MongoDB failed: " + str(err))
            raise err

    def __del__(self):
        self.__client.close()

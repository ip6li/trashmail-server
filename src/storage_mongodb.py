from pymongo import MongoClient
from pymongo import errors
from config import Config
from logger import Logger


class Mongo:
    __client = MongoClient(Config.getMongoURL())
    __db = __client[Config.getDB()]

    @staticmethod
    def insert (data):
        from pymongo.errors import ServerSelectionTimeoutError
        try:
            posts = Mongo.__db.posts
            post_id = posts.insert_one(data).inserted_id
            return post_id
        except ServerSelectionTimeoutError as err:
            Logger.warn("Cannot connect to MongoDB server: " + str(err))
        except errors as err:
            Logger.warn("MongoDB failed: " + str(err))

        return None

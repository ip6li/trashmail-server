from pymongo import MongoClient
from pymongo import errors
from config import Config


class Mongo:
    __client = MongoClient(Config.getMongoURL())
    __db = __client[Config.getDB()]

    @staticmethod
    def insert (data):
        try:
            posts = Mongo.__db.posts
            post_id = posts.insert_one(data).inserted_id
            return post_id
        except errors as err:
            print ("MongoDB failed: ", err)
            return None

# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pymongo import errors
from config import Config
from logger import Logger
from custom_cb import retry_auto_reconnect


class Mongo:

    @retry_auto_reconnect
    def __init__(self):
        self.__client = MongoClient(host=Config.getMongoURL(), socketTimeoutMS=Config.getTimeout())
        self.__db = self.__client[Config.getDB()]
        self.__log = Logger(__name__)

    @retry_auto_reconnect
    def insert(self, data):
        from pymongo.errors import ServerSelectionTimeoutError
        try:
            posts = self.__db.posts
            post_id = posts.insert_one(data).inserted_id
            return post_id
        except ServerSelectionTimeoutError as err:
            self.__log.warn("Cannot connect to MongoDB server: " + str(err))
            raise err
        except errors as err:
            self.__log.warn("MongoDB failed: " + str(err))
            raise err

    def __del__(self):
        self.__client.close()

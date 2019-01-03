#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pymongo import MongoClient
from config import Config


class Cleanup:

    @staticmethod
    def __getPosts():
        client = MongoClient(Config.getMongoURL())
        db = client[Config.getDB()]
        return db.posts

    @staticmethod
    def delete(fromtime):
        posts = Cleanup.__getPosts()
        query = {"timestamp": {"$lt": fromtime}}
        res = posts.delete_many(query)
        print(res.deleted_count, " documents deleted.")

    @staticmethod
    def list(fromtime):
        posts = Cleanup.__getPosts()
        query = {"timestamp": {"$lt": fromtime}}
        for post in posts.find(query):
            print(post)

    @staticmethod
    def deleteAll():
        posts = Cleanup.__getPosts()
        query = {}
        res = posts.delete_many(query)
        print(res.deleted_count, " documents deleted.")


now = int(time.time())
from_del_time = now - Config.getMaxAge()
#Cleanup.list(now)
Cleanup.delete(from_del_time)

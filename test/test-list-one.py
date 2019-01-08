#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../src")
import unittest
from testlib import Testlib


class Test1(unittest.TestCase):

    def test_readMail(self):
        user = "joe.test.0@example.com"
        posts = Testlib.getPosts()
        for post in posts.find({"X-Original-To": user}):
            print(post)


if __name__ == '__main__':
    unittest.main()

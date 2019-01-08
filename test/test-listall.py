#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
from testlib import Testlib


class Test2(unittest.TestCase):

    def test_list(self):
        now = int(time.time())
        Testlib.list(now)
        print("success")
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

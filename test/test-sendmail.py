#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../src")
import unittest
from testlib import Testlib


class Test1(unittest.TestCase):

    def test_genMails(self):
        count = 10
        res = True
        for i in range(count):
            u = "joe.test."+str(i)+"@example.com"
            Testlib.sendMail(u)

        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()

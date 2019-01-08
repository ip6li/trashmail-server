#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../src")
import unittest
from testlib import Testlib


class Test1(unittest.TestCase):

    def test_genMails_1(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = "Joe Test <joe.test.to@example.com>"
            smtp.sendMail(u, None, None)
        del smtp
        self.assertTrue(res)

    def test_genMails_2(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = "Joe Test <joe.test.cc@example.com>"
            smtp.sendMail(None, u, None)
        del smtp
        self.assertTrue(res)

    def test_genMails_3(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = "Joe Test <joe.test.bcc@example.com>"
            smtp.sendMail(None, None, u)
        del smtp
        self.assertTrue(res)

    def test_genMails_4(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = ["Joe Test <joe.test.to@example.com>", "Some Other User <some.other.user@exmaple.org>"]
            smtp.sendMail(u, None, None)
        del smtp
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()

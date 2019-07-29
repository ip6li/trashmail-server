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
            u = "Joe Test To <joe.test@example.com>"
            smtp.sendMail(u, None, None)
        del smtp
        self.assertTrue(res)

    def test_genMails_2(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = "Joe Test CC <joe.test@example.com>"
            smtp.sendMail(None, u, None)
        del smtp
        self.assertTrue(res)

    def test_genMails_3(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = "Joe Test BCC <joe.test@example.com>"
            smtp.sendMail(None, None, u)
        del smtp
        self.assertTrue(res)

    def test_genMails_4(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = ["Joe Test Multiple <joe.test@example.com>", "Some Other User <some.other.user@example.org>"]
            smtp.sendMail(u, None, None)
        del smtp
        self.assertTrue(res)

    def test_genMails_5(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = ["Joe Test Uppercase <Joe.Test@example.com>"]
            smtp.sendMail(u, None, None)
        del smtp
        self.assertTrue(res)

    def test_genMails_6(self):
        smtp = Testlib()
        count = 1
        res = True
        for i in range(count):
            u = ["Long Name 32 Chars <d644738e086d4da5e339bbaea6fb50e3@example.com>"]
            smtp.sendMail(u, None, None)
        del smtp
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()

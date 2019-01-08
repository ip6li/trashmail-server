#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../src")
import unittest
from logger import Logger


class Test1(unittest.TestCase):
    Logger.init()
    Logger.crit("Test critical")
    Logger.warn("Test warning")
    Logger.info("Test info")
    Logger.debug("Test debug")

if __name__ == '__main__':
    unittest.main()

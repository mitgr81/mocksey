#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mocksey import generate_mock

import unittest


class BoisterousBagel(object):
    pass


class SimpleMockTestCase(unittest.TestCase):

    def setUp(self):
        self.mock = generate_mock(BoisterousBagel)

    def test_mock_steals_class_name(self):
        """ mocksey.generate_mock: Mock "inherits" mocked class name"""
        self.assertEqual('BoisterousBagel', self.mock.__class__.__name__)

if __name__ == '__main__':
    unittest.main()

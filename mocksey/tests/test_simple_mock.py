#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mocksey import generate_mock  # SUT

import random
import unittest

TEETH_PROP = '%d wombat teeth are full of ouch' % random.randint(0, 30)


class WileyWombat(object):
    teeth = TEETH_PROP

    def masticate(self):
        while True:
            pass


class SimpleMockTestCase(unittest.TestCase):

    def setUp(self):
        self.mock = generate_mock(WileyWombat)

    def test_mock_steals_class_name(self):
        """ mocksey.generate_mock: Mock "inherits" mocked class name"""
        self.assertEqual('WileyWombat', self.mock.__class__.__name__, "Mock did not inherit class name")

    def test_mock_reports_itself_as_mock(self):
        """ mocksey.generate_mock: Mock's repr reveals it's true nature"""
        self.assertEqual("MockWileyWombat", '%s' % self.mock, "Mock did not identify as mock in repr")

    def test_mock_inherits_attributes(self):
        """ mocksey.generate_mock: Attributes on mocked class get mirrored onto mock"""
        self.assertTrue(hasattr(self.mock, 'teeth'), "Mock does not have an attribute that the mocked object did")
        self.assertEqual(TEETH_PROP, self.mock.teeth, "Mock's value was not set correctly.")

    def test_mock_inherits_callable(self):
        """ mocksey.generate_mock: Methods on mocked class are mirrored and emptied"""
        self.assertTrue(hasattr(self.mock, 'masticate'), "Mock does not have a method that the mocked object did")
        self.mock.masticate()

if __name__ == '__main__':
    unittest.main()

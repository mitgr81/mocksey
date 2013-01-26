#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mocksey import generate_mock  # SUT

import random
import unittest
from nose.tools import assert_equals

import sys
if sys.version_info < (3,):
    range = xrange

TEETH_PROP = '%d wombat teeth are full of ouch' % random.randint(0, 30)


class WileyWombat(object):
    teeth = TEETH_PROP

    def masticate(self):
        while True:
            pass


class WombatMob(object):

    def __init__(self, a_wombat):
        self.wombat = a_wombat

    def feed(self):
        return self.wombat.masticate()


class SimpleMockTestCase(unittest.TestCase):

    def setUp(self):
        self.mock = generate_mock(WileyWombat)
        self.mob = WombatMob(self.mock)

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

    def test_mock_returns(self):
        """ mocksey.MockObject: Mocked function returns requested value """
        masticate_return = "Okay okay, I'll chew it up!"
        self.mock.returns('masticate', masticate_return)
        self.assertEqual(masticate_return, self.mob.feed())

    def test_mock_returns_at(self):
        """ mocksey.MockObject: Mocked function returns requested value at requested index """
        masticate_return = "Okay okay, I'll chew it up attempt %d!"
        for trial in range(random.randint(2, 15)):
            self.mock.returns_at(trial, 'masticate', masticate_return % (trial + 1))
            self.assertEqual(masticate_return % (trial + 1), self.mob.feed())

    def test_mock_expect_once(self):
        """ mocksey.MockObject: Mock blows up if an expected function is not called """
        self.mock.expect_once('masticate')
        try:
            self.mock.run_asserts(assert_equals)
            raise Exception("Did not blow when an expected function was not called")  # Can't rely on self.fail, as that's an AssertionError
        except AssertionError:
            pass  # we want it to kablooey this way, hooray!

    def test_mock_expect_multiple(self):
        """ mocksey.MockObject: Mock blows up if an expected function is not called """
        call_count = random.randint(1, 50)
        self.mock.expect_call_count('masticate', call_count)
        for waffle in range(call_count):
            self.mock.masticate()
        try:
            self.mock.run_asserts(assert_equals)
            raise Exception("Did not blow when an expected function was not called enough")  # Can't rely on self.fail, as that's an AssertionError
        except AssertionError:
            pass  # we want it to kablooey this way, hooray!

        self.mock.masticate()
        self.mock.run_asserts()

if __name__ == '__main__':
    unittest.main()

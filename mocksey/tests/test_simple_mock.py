#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest

from mocksey import MockseyObject, generate_mock  # SUT

TEETH_PROP = "%d wombat teeth are full of ouch" % random.randint(0, 30)


class WileyWombat:
    teeth = TEETH_PROP

    def masticate(self):
        while True:
            pass

    def patty_pat(self, patting_device):
        while True:
            print("blowing up your tests now, kthxbie")

    def perform(self, **feat):
        while True:
            print("Now {}-ifying {}".format(feat.items()[0]))


class WombatMob:
    def __init__(self, a_wombat):
        self.wombat = a_wombat

    def feed(self):
        return self.wombat.masticate()

    def pat(self, patting_device="face"):
        return self.wombat.patty_pat(patting_device)

    def perform(self, **feat):
        return self.wombat.perform(**feat)

    def do_yer_business(self):
        return self.wombat.defecate()


class SimpleMockTestCase(unittest.TestCase):
    def setUp(self):
        self.mock = generate_mock(WileyWombat)
        self.mob = WombatMob(self.mock)

    def test_mock_steals_class_name(self):
        """mocksey.generate_mock: Mock "inherits" mocked class name"""
        self.assertEqual("WileyWombat", self.mock.__class__.__name__, "Mock did not inherit class name")

    def test_mock_reports_itself_as_mock(self):
        """mocksey.generate_mock: Mock's repr reveals it's true nature"""
        self.assertEqual("MockWileyWombat", "{}".format(self.mock), "Mock did not identify as mock in repr")

    def test_mock_inherits_attributes(self):
        """mocksey.generate_mock: Attributes on mocked class get mirrored onto mock"""
        self.assertTrue(hasattr(self.mock, "teeth"), "Mock does not have an attribute that the mocked object did")
        self.assertEqual(TEETH_PROP, self.mock.teeth, "Mock's value was not set correctly.")

    def test_mock_inherits_callable(self):
        """mocksey.generate_mock: Methods on mocked class are mirrored and emptied"""
        self.assertTrue(hasattr(self.mock, "masticate"), "Mock does not have a method that the mocked object did")
        self.mock.masticate()

    def test_mock_returns(self):
        """mocksey.MockseyObject: Mocked function returns requested value"""
        masticate_return = "Okay okay, I'll chew it up!"
        self.mock.returns("masticate", masticate_return)
        self.assertEqual(masticate_return, self.mob.feed())

    def test_mock_returns_at(self):
        """mocksey.MockseyObject: Mocked function returns requested value at requested index"""
        masticate_return = "Okay okay, I'll chew it up attempt %d!"
        for trial in range(random.randint(2, 15)):
            self.mock.returns_at(trial, "masticate", masticate_return % (trial))
            self.assertEqual(masticate_return % (trial), self.mob.feed())

    def test_unexpected_calls_are_tracked(self):
        """mocksey.MockseyObject: Mocksey keeps track of method calls even when they're not being asserted"""
        call_count = random.randint(1, 50)
        for call_time in range(call_count):
            self.mob.pat()

        self.assertEqual(call_count, self.mock.called_functions["patty_pat"]["count"])

    def test_unexpected_calls_track_args(self):
        """mocksey.MockseyObject: Mocksey keeps track of method call args even when they're not being asserted"""
        pattable_patting_parts = ["Hand", "cheek", "foot", "toe", "30-foot pole"]
        choice = random.choice(pattable_patting_parts)
        self.mob.pat(choice)
        self.assertEqual((choice,), self.mock.called_functions["patty_pat"][0]["args"])

    def test_unexpected_calls_track_kwargs(self):
        """mocksey.MockseyObject: Mocksey keeps track of method call kwargs even when they're not being asserted"""
        amazing_wombat_actions = [
            {"fly": "faster than light"},
            {"dig": "like a boss"},
            {"trample": "armies of zombies"},
            {"shoot": "Space-mutants with eye lazorz"},
            {"speak": "perfect Russian"},
            {"dance": "all teh koalas"},
            {"be": "cute...or says my wife", "scare": "all the crawdillys out"},
            {"lead": "super duper secret life of crime, villany and wombatery"},
        ]
        choice = random.choice(amazing_wombat_actions)
        self.mob.perform(**choice)

        self.assertEqual(choice, self.mock.called_functions["perform"][0]["kwargs"])

    def test_raises(self):
        """mocksey.MockseyObject: Mocksey can raise on a given function call"""

        class ZombieInvasion(Exception):
            pass

        self.mock.raises("defecate", ZombieInvasion)

        try:
            self.mob.do_yer_business()
            self.fail("Did not raise as expected")
        except ZombieInvasion:
            pass  # Just as I had feared!  All the Safety Wombats will be constipated during the Zombie Invasion

    def test_supports_with_statement(self):
        """mocksey.MockseyObject: Mocksey mocks can be used in python's 'with' statement"""
        with MockseyObject() as mocksey:
            mocksey.expect_once("something")


# test module mocking...i.e. import something like smtp and set a mock on smtp.SMTP

if __name__ == "__main__":
    unittest.main()

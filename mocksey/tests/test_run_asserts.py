#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest

from mocksey import generate_mock  # SUT

TEETH_PROP = "%d wombat teeth are full of ouch" % random.randint(0, 30)


class TestDummy(unittest.TestCase):
    def nop(self):
        pass


assert_equals = TestDummy().assertEqual


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

    def move(self, *args, **kwargs):
        while True:
            pass


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

    def test_mock_expect_once(self):
        """mocksey.MockseyObject: Mock blows up if an expected function is not called"""
        self.mock.expect_once("masticate")
        try:
            self.mock.run_asserts(assert_equals)
            # Can't rely on self.fail, as that's an AssertionError
            raise Exception("Did not blow up when an expected function was not called")
        except AssertionError:
            pass  # we want it to kablooey this way, hooray!

    def test_mock_expect_multiple(self):
        """mocksey.MockseyObject: Mock blows up if an expected function is not called"""
        call_count = random.randint(1, 50)
        self.mock.expect_call_count("masticate", call_count)
        for waffle in range(call_count - 1):
            self.mock.masticate()
        try:
            self.mock.run_asserts(assert_equals)
            # Can't rely on self.fail, as that's an AssertionError
            raise Exception("Did not blow up when an expected function was not called enough")
        except AssertionError:
            pass  # we want it to kablooey this way, hooray!

        self.mock.masticate()
        self.mock.run_asserts()

    def test_mock_expect_never(self):
        """mocksey.MockseyObject: Mock blows up if an function who is supposed to never be called is called"""
        self.mock.expect_never("go_crazygonuts")
        self.mock.go_crazygonuts()

        try:
            self.mock.run_asserts(assert_equals)
            # Can't rely on self.fail, as that's an AssertionError
            raise Exception("Did not blow up when a function that we expected to never be called was called")
        except AssertionError:
            pass  # we want it to kablooey this way, hooray!

    ############################# ARG VERIFICATION ##################################

    def test_mock_validates_args_for_single_call(self):
        """mocksey.MockseyObject.run_asserts: run_asserts properly complains when single call has wrong args"""

        self.mock.expect_once("move", args=("north", "south"))
        self.mock.move("nerth", "serth")
        try:
            self.mock.run_asserts()
            raise Exception("Did not blow up when an expected function was called with unexpected args")
        except AssertionError:
            pass

    def test_mock_validates_any_args_for_single_wildcard_call(self):
        """mocksey.MockseyObject.run_asserts: run_asserts is happy with any args when args aren't specified"""

        self.mock.expect_once("move")
        self.mock.move("nerth", "serth")
        self.mock.run_asserts()

    def test_mock_validates_args_for_multiple_calls(self):
        """
        mocksey.MockseyObject.run_asserts: run_asserts properly complains when one or all of multiple calls has wrong
        args
        """
        self.mock.expect_at("move", 2, args=("east", "butter"))
        self.mock.expect_at("move", 0, args=("north", "south"))
        self.mock.move("north", "south")
        self.mock.move("north", "crooked")
        self.mock.move("yeast", "buttermilk")
        try:
            self.mock.run_asserts()
            raise Exception("Did not blow up when an expected function was called with unexpected args")
        except AssertionError:
            pass

    ############################# KWARG VERIFICATION ##################################

    def test_mock_validates_kwargs_for_single_call(self):
        """mocksey.MockseyObject.run_asserts: run_asserts properly complains when call has wrong kwargs"""

        self.mock.expect_once("move", kwargs={"north": 600, "south": 900})
        self.mock.move(north=900, south=500, dance_style="chicken-headed two-step")
        try:
            self.mock.run_asserts()
            raise Exception("Did not blow up when an expected function was called with unexpected kwargs")
        except AssertionError:
            pass

    def test_mock_validates_any_kwargs_for_single_wildcard_call(self):
        """mocksey.MockseyObject.run_asserts: run_asserts is happy with any kwargs when args aren't specified"""

        self.mock.expect_once("move")
        self.mock.move(north=540, south=690)
        self.mock.run_asserts()

    def test_mock_validates_kwargs_for_multiple_calls(self):
        """
        mocksey.MockseyObject.run_asserts: run_asserts properly complains when one or all of multiple calls has wrong
        kwargs
        """
        self.mock.expect_at("move", 2, kwargs={"north": 600, "south": 900})
        self.mock.expect_at("move", 0, kwargs={"north": 554, "south": 224})

        self.mock.move(north=554, south=224)
        self.mock.move(north=424, south=585)
        self.mock.move(north=540, south=234)
        try:
            self.mock.run_asserts()
            raise Exception("Did not blow up when an expected function was called with unexpected kwargs")
        except AssertionError:
            pass


if __name__ == "__main__":
    unittest.main()

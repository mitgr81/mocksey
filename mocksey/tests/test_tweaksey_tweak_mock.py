#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest import mock

from mocksey import tweaksey  # SUT


class TweakseyTweaksMockCase(unittest.TestCase):
    def setUp(self):
        self.ncm_acow = mock.NonCallableMock.assert_called_once_with
        self.ncm_acw = mock.NonCallableMock.assert_called_with
        self.ncm_aac = mock.NonCallableMock.assert_any_call
        tweaksey.tweak_mock(mock)

        self.some_mock = mock.MagicMock()

    def tearDown(self):
        mock.NonCallableMock.assert_called_with = self.ncm_acw
        mock.NonCallableMock.assert_called_once_with = self.ncm_acow
        mock.NonCallableMock.assert_any_call = self.ncm_aac

    def test_monkey_patching(self):
        """mocksey.tweaksey.tweak_mock: tweaksey monkey patches / duck punches mock's methods"""
        self.assertIn("tweaksey", str(mock.NonCallableMock.assert_any_call.__code__))
        self.assertIn("tweaksey", str(mock.NonCallableMock.assert_called_once_with.__code__))
        self.assertIn("tweaksey", str(mock.NonCallableMock.assert_called_with.__code__))

    def test_assert_called_once_with_override_assert_any_message_with_bad_arg(self):
        """mocksey.tweaksey.tweak_mock.assert_called_once_with: Override message for arg match failure"""
        self.some_mock()
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_called_once_with("pants")

        actual = str(con_man.exception)
        expected = "Suffered the following call issues (expected != actual):\n"
        self.assertIn(expected, actual)
        expected = "Args:  Tuples differ: ('pants',) != ()\n\nFirst tuple contains 1 additional elements.\nFirst extra element 0:\n'pants'\n\n- ('pants',)\n+ ()\n"
        self.assertIn(expected, actual)
        expected = "Kwargs: Nothing!"
        self.assertIn(expected, actual)

    def test_assert_called_once_with_override_assert_any_message_with_bad_kwarg(self):
        """mocksey.tweaksey.tweak_mock.assert_called_once_with: Override message for kwarg match failure"""
        self.some_mock()
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_called_once_with(clothing="pants")

        actual = str(con_man.exception)
        expected = "Suffered the following call issues (expected != actual):\n"
        self.assertIn(expected, actual)
        expected = "Args:  Nothing!\n"
        self.assertIn(expected, actual)
        expected = "Kwargs: {'clothing': 'pants'} != {}\n- {'clothing': 'pants'}\n+ {}"
        self.assertIn(expected, actual)

    def test_assert_called_once_with_dont_interfere_when_call_was_good(self):
        """mocksey.tweaksey.tweak_mock.assert_called_once_with: Don't raise without a failure"""
        self.some_mock("pants")
        try:
            self.some_mock.assert_called_once_with("pants")  # SUT
        except AssertionError:
            self.fail("I know this test looks funny, but I need to make sure we don't accidentally raise")

    def test_assert_called_once_with_missing_call(self):
        """mocksey.tweaksey.tweak_mock.assert_called_once_with: Don't raise without a failure"""
        self.some_mock.__str__.return_value = "lalalalala"

        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_called_once_with(clothing="pants")

        actual = str(con_man.exception)
        expected = "Mock 'lalalalala' expected to be called once. Called 0 times with []."
        self.assertIn(expected, actual)

    #######################################

    def test_assert_called_with_override_assert_any_message_with_bad_arg(self):
        """mocksey.tweaksey.tweak_mock.assert_called_with: Override message for arg match failure"""
        self.some_mock()
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_called_with("pants")

        actual = str(con_man.exception)
        expected = "Suffered the following call issues (expected != actual):\n"
        self.assertIn(expected, actual)
        expected = (
            "Args:  Tuples differ: ('pants',) != ()\n\nFirst tuple contains 1 additional elements."
            "\nFirst extra element 0:\n'pants'\n\n- ('pants',)\n+ ()\n"
        )
        self.assertIn(expected, actual)
        expected = "Kwargs: Nothing!"
        self.assertIn(expected, actual)

    def test_assert_called_with_override_assert_any_message_with_bad_kwarg(self):
        """mocksey.tweaksey.tweak_mock.assert_called_with: Override message for kwarg match failure"""
        self.some_mock()
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_called_with(clothing="pants")

        actual = str(con_man.exception)
        expected = "Suffered the following call issues (expected != actual):\n"
        self.assertIn(expected, actual)
        expected = "Args:  Nothing!\n"
        self.assertIn(expected, actual)
        expected = "Kwargs: {'clothing': 'pants'} != {}\n- {'clothing': 'pants'}\n+ {}"
        self.assertIn(expected, actual)

    def test_assert_called_with_dont_interfere_when_call_was_good(self):
        """mocksey.tweaksey.tweak_mock.assert_called_with: Don't raise without a failure"""
        self.some_mock("pants")
        try:
            self.some_mock.assert_called_with("pants")  # SUT
        except AssertionError:
            self.fail("I know this test looks funny, but I need to make sure we don't accidentally raise")

    def test_assert_called_with_missing_call(self):
        """mocksey.tweaksey.tweak_mock.assert_called_with: Don't raise without a failure"""
        self.some_mock.__str__.return_value = "dadadada"

        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_called_with(clothing="pants")

        actual = str(con_man.exception)
        expected = "Mock 'dadadada' was never called."
        self.assertEqual(expected, actual)

    #######################################

    # test single calls fall through
    def test_assert_any_call_override_assert_any_message_with_bad_arg(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Override message for arg match failure"""
        self.some_mock()
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_any_call("pants")

        actual = str(con_man.exception)
        expected = "Suffered the following call issues (expected != actual):\n"
        self.assertIn(expected, actual)
        expected = (
            "Args:  Tuples differ: ('pants',) != ()\n\nFirst tuple contains 1 additional elements."
            "\nFirst extra element 0:\npants\n\n- ('pants',)\n+ ()\n"
        )
        self.assertIn(expected, actual)
        expected = "Kwargs: Nothing!"
        self.assertIn(expected, actual)

    def test_assert_any_call_override_assert_any_message_with_bad_kwarg(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Override message for kwarg match failure"""
        self.some_mock()
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_any_call(clothing="pants")

        actual = str(con_man.exception)
        expected = "Suffered the following call issues (expected != actual):\n"
        self.assertIn(expected, actual)
        expected = "Args:  Nothing!\n"
        self.assertIn(expected, actual)
        expected = "Kwargs: {'clothing': 'pants'} != {}\n- {'clothing': 'pants'}\n+ {}"
        self.assertIn(expected, actual)

    # test multiple calls
    def test_assert_any_call_override_assert_any_message_with_bad_arg(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Override message for arg match failure"""
        self.some_mock()
        self.some_mock("yes again")
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_any_call("pants")

        actual = str(con_man.exception)
        expected = "mock('pants') call not found among:\n\t[call(), call('yes again')]"
        self.assertEqual(expected, actual)

    def test_assert_any_call_override_assert_any_message_with_bad_kwarg(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Override message for kwarg match failure"""
        self.some_mock()
        self.some_mock(and_again=True)
        self.some_mock("once", "more")
        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_any_call(clothing="pants")

        actual = str(con_man.exception)
        expected = (
            "mock(clothing='pants') call not found among:\n\t[call(), call(and_again=True), call('once', 'more')]"
        )
        self.assertEqual(expected, actual)

    # test multiple calls with named mocks
    def test_assert_any_call_override_assert_any_message_with_bad_arg(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Override message for arg match failure"""
        local_mock = mock.MagicMock(name="the_doctor")
        local_mock()
        local_mock("yes again")
        with self.assertRaises(AssertionError) as con_man:
            local_mock.assert_any_call("pants")

        actual = str(con_man.exception)
        expected = "the_doctor('pants') call not found among:\n\t[the_doctor(), the_doctor('yes again')]"
        self.assertEqual(expected, actual)

    def test_assert_any_call_override_assert_any_message_with_bad_kwarg(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Override message for kwarg match failure"""
        local_mock = mock.MagicMock(name="the_doctor")
        local_mock()
        local_mock(and_again=True)
        local_mock("once", "more")
        with self.assertRaises(AssertionError) as con_man:
            local_mock.assert_any_call(clothing="pants")

        actual = str(con_man.exception)
        expected = (
            "the_doctor(clothing='pants') call not found among:"
            "\n\t[the_doctor(), the_doctor(and_again=True), the_doctor('once', 'more')]"
        )
        self.assertEqual(expected, actual)

    def test_assert_any_call_dont_interfere_when_call_was_good(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Don't raise without a failure"""
        self.some_mock("slippers")
        self.some_mock("pants")
        self.some_mock(1234)
        try:
            self.some_mock.assert_any_call("pants")  # SUT
        except AssertionError:
            self.fail("I know this test looks funny, but I need to make sure we don't accidentally raise")

    def test_assert_any_call_missing_call(self):
        """mocksey.tweaksey.tweak_mock.assert_any_call: Don't raise without a failure"""
        self.some_mock.__str__.return_value = "dadadada"

        with self.assertRaises(AssertionError) as con_man:
            self.some_mock.assert_any_call(clothing="pants")

        actual = str(con_man.exception)
        expected = "Mock 'dadadada' was never called."
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for several functionalities."""

from numpy import float64
from unittest import TestCase

from main import main
from scripts.utils import convert_binary_to_decimal


def assert_binary_output(test_string):
    """Assert that the input string is actually a binary representation.

    Parameters
    ----------
    test_string: str
        Should be a binary representation, e.g. '100001'

    Returns
    -------
    out: bool
        Flag indicating whether the assertion is true, or not.
    """
    # Test that the string consists only of 1s and 0s
    for val in test_string:
        if val not in ['0', '1']:
            return False

    # Attempt a conversion
    try:
        convert_binary_to_decimal(test_string)
        return True
    except ValueError:
        return False


class Test(TestCase):

    def test(self):

        frequency_test_value = 200000

        numerical_values, messages = main(frequency_test_value)

        assert assert_binary_output(numerical_values[0])
        assert assert_binary_output(numerical_values[1])
        assert assert_binary_output(numerical_values[2])

        self.assertEqual(type(numerical_values[3]), float64)

        self.assertEqual(type(messages[0]), str)
        self.assertEqual(type(messages[1]), str)

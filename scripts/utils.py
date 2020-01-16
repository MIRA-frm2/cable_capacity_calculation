# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utilities and helper functions."""


def add_inverse(a, b):
    """Adds two values as a parallel connection.

    Parameters
    ----------
    a: float, ndarray
    b: float, ndarray

    Returns
    -------
    out: float
        the inverse of the sum of their inverses
    """
    if a and b:
        return (a**(-1) + b**(-1))**(-1)
    else:
        return 0


def convert_decimal_to_binary(number):
    """

    Parameters
    ----------
    number: int

    Returns
    -------
    out: str

    >>> convert_decimal_to_binary(10)
    '1010'
    """
    return bin(number)[2:]


def convert_binary_to_decimal(binary_number):
    """

    Parameters
    ----------
    binary_number

    Returns
    -------

    >>> convert_binary_to_decimal('1010')
    10
    """
    decimal = 0
    i = 0
    n = len(binary_number) - 1
    for bit in binary_number:
        decimal += + int(bit) * pow(2, n - i)
        i += 1
    return decimal

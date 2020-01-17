# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utilities and helper functions."""

import csv
import numpy as np


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


def read_data_from_file(file_name):
    """Read data from file.

    Parameters
    ----------
    file_name: str
        Name of the file to be read from.
    """
    _frequency = list()
    _capacity_1 = list()
    _capacity_2 = list()
    connection_type = list()

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if row[1] and row[2] and row[3]:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    try:
                        _frequency.append(float(row[0]))
                        _capacity_1.append(float(row[1]))
                        _capacity_2.append(float(row[2]))

                        connection_type.append(int(row[3]))
                    except IndexError:
                        print("wtf")

        return np.asarray(_frequency), np.asarray(_capacity_1), np.asarray(_capacity_2), np.asarray(connection_type)

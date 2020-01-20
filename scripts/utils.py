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


def transform_frequency(eigenfrequency_value, prefactor=3.8/143000):
    """Transform eigenfrequency to match the Larmor precesion.

    # ToDo: need more info on this

    Parameters
    ----------
    eigenfrequency_value: float
        Eigenfrequency to be converted.
    prefactor: float, optional
        #Todo: Draft
        Conversion factor that matches the data.
        Defaults to 3.8/143000

    Returns
    -------
    out: float
    """
    return prefactor * eigenfrequency_value


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


def read_capacities_data_from_file(file_name):
    """Read data from file.

    Parameters
    ----------
    file_name: str
        Name of the file to be read from.
    """
    capacities = list()
    index_1 = list()
    index_2 = list()
    index_3 = list()
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
                        capacities.append(float(row[0]))

                        index_1.append(float(row[1]))
                        index_2.append(float(row[2]))
                        index_3.append(float(row[3]))

                        connection_type.append(int(row[4]))
                    except IndexError:
                        print("wtf")

        return np.asarray(capacities), np.asarray(index_1), np.asarray(index_2), np.asarray(index_3), \
               np.asarray(connection_type)


def save_capacities_data_to_file(data, file_name, extension='.csv'):
    """Save data to file."""
    if extension in file_name:
        full_filename = file_name
    else:
        full_filename = f'{file_name}{extension}'

    with open(full_filename, 'w') as file:

        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(["capacity", "c1_box_index", "c2_box_index", "c3_box_index", "connection_type"])

        for capacity, connection_data in data.items():
            row = list((capacity, connection_data[0], connection_data[1], connection_data[2], connection_data[3]))

            csv_writer.writerow(row)

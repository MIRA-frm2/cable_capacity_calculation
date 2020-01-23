# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Several computation functions for the capacities."""


import numpy as np

from scripts.capacity_boxes import capacity_box_1, capacity_box_2, capacity_box_3
from scripts.utils import add_inverse
from scripts.parameters import inductance


def parasitic_capacity_calculation(capacity, effective_frequency, connection_type='parallel'):
    """Compute the parasitic capacity assuming that it contributes either as a serial or parallel connection.

    Parameters
    ----------
    capacity: float
        Measured capacity.
    effective_frequency: float
        Measured effective frequency.
    connection_type: str, optional
        Either 'serial' or 'parallel'.
        Defaults to 'serial'.

    Returns
    -------
    out: float
        Parasitic capacity.
    """
    capacity_theo = (2 * np.pi * effective_frequency) ** -2 / inductance
    if connection_type == 'serial':
        return capacity_theo - capacity
    else:
        return capacity_theo * capacity / (capacity - capacity_theo)


def compute_capacity_values(capacity_1, capacity_2, connection_type):
    """Compute the capacity values from the data table.

    Parameters
    ----------
    capacity_1: ndarray
    capacity_2: ndarray
    connection_type: ndarray

    Returns
    -------
    capacity_values: ndarray
        List of capacity values.
    """
    capacity_values = []
    for i in range(len(capacity_1)):
        capacity_values.append(compute_capacity(capacity_1[i], capacity_2[i], serial=connection_type[i]))
    return np.asarray(capacity_values)


def compute_capacity(c1, c2, c3=0, serial=0):
    """Compute the capacity values from the frequency data table.

    Parameters
    ----------
    c1: int
        Index for the first capacity box.
    c2: int
        Index for the second capacity box.
    c3: int, optional
        Index for the third capacity box.
        Defaults to 0.
    serial: int
        Flag indicating whether to connect the boxes in series or in parallel.
    Returns
    -------
    out: float
        Capacity.

    >>> compute_capacity(5, 4, 0, 1)
    1.9655172413793106e-09
    """
    if serial == 0:
        cbox1 = capacity_box_1.index_to_capacity(int(c1)) + capacity_box_2.index_to_capacity(int(c2))
    elif serial == 1:
        cbox1 = add_inverse(capacity_box_1.index_to_capacity(int(c1)), capacity_box_2.index_to_capacity(int(c2)))
    else:
        cbox1 = None

    cbox2 = capacity_box_3.index_to_capacity(c3)

    if cbox2 == 0:
        return cbox1 * 1e-9
    elif cbox1 == 0:
        return cbox2 * 1e-9
    else:
        return add_inverse(cbox1 * 1e-9, cbox2 * 1e-9)


def compute_total_capacity(c1, c2, c3, serial):
    """Compute the total capacity from the three boxes.

    Parameters
    ----------
    c1: float
        First box capacity, can be connected either in serial or in parallel.
    c2: float
        Second box capacity, can be connected either in serial or in parallel.
    c3: float
        Third box capacity, can be connected only in serial.
    serial: bool
        Flag indicating whether to connected the first two boxes in serial or in parallel.

    Returns
    -------
    c_total: float
        Total capacity of the circuit.
    """
    if serial == 0:
        c12 = c1 + c2
    else:
        c12 = add_inverse(c1, c2)

    c_total = add_inverse(c12, c3)

    return c_total

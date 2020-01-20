# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Compute all possible capacities."""


from scripts.index_capacity_class import capacity_box_1, capacity_box_2, capacity_box_3
from scripts.utils import add_inverse, save_capacities_data_to_file, read_capacities_data_from_file


def compute_all_possible_capacities():
    """Compute all the experimental possible capacities from the values at hand."""
    data = dict()

    for val_c1 in range(capacity_box_1.max_index):
        for val_c2 in range(capacity_box_2.max_index):
            for val_c3 in range(capacity_box_3.max_index):
                for serial in [0, 1]:
                    data[compute_capacity(val_c1, val_c2, val_c3, serial=serial)] = (val_c1, val_c2, val_c3, serial)

    save_capacities_data_to_file(data, '../data/capacities.csv')


def compute_capacity(c1, c2, c3=0, serial=0):
    """Compute the capacity values from the data table.

    Parameters
    ----------
    c1
    c2
    c3
    serial

    Returns
    -------
    out: float
        Capacity.
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


def find_best_capacity_value(desired_capacity):
    """Return the closest capacity to the desired one from the possible capacity combinations.

    Parameters
    ----------
    desired_capacity: float
        The desired capacity value needed for the circuit.

    Returns
    -------
    best_capacity: float
    error: float
        The difference between the output and the desired capacity.
    connection_data: tuple
        Tuple containing the indexes for the capacity boxes and the connection type (serial/parallel).
    """
    values = read_capacities_data_from_file('data/capacities.csv')

    best_capacity = 0
    error = desired_capacity
    connection_data = None

    for i in range(len(values[0])):
        value = values[0][i]
        new_error = abs(value - desired_capacity)

        if new_error < error:
            best_capacity = value
            error = new_error

            connection_data = values[1][i], values[2][i], values[3][i], values[4][i]

    return best_capacity, error, connection_data


def compute_index(capacity, from_data_table=True):
    """Compute the index from the given capacity.

    Strongly recommended: use the data table.
    Can be done either from the computed capacities table or computed directly the from equations.

    Parameters
    ----------
    capacity: float
        Capacity value to be converted to index.
    from_data_table: bool, optional
        Flag indicating whether to use the data table or to compute from scratch.
        Defaults to True.

    Returns
    -------
    message: str
        Message to be printed.
    numerical_output: tuple
        Tuple of values containing:

        val_index_c1: int
            The index value for the first capacity box.
        val_index_c2: int
            The index value for the second capacity box.
        val_index_c3: int
            The index value for the third capacity box.
        remainder_capacity: float
            The difference between the desired capacity and the output capacity.
    """
    if from_data_table:
        best_capacity, remainder_capacity, connection_data = find_best_capacity_value(capacity)
        val_index_c1, val_index_c2, val_index_c3, connection_type = connection_data
    else:

        val_index_c1, remainder_capacity = capacity_box_1.capacity_to_index(capacity)
        val_index_c2, remainder_capacity = capacity_box_2.capacity_to_index(remainder_capacity)
        val_index_c3, remainder_capacity = capacity_box_3.capacity_to_index(remainder_capacity)

        best_capacity = capacity - remainder_capacity

        connection_type = 1

    message = f'The closest possible capacity value is: {best_capacity}\n' \
              f'With the capacity error of: {remainder_capacity}\n' \
              f'\nThe indexes are as follows:\n' \
              f'From the C1box: {val_index_c1}\n' \
              f'From the C2box: {val_index_c2}\n' \
              f'From the C3box: {val_index_c3}\n' \
              f'Connected in serial: {connection_type}'

    return [val_index_c1, val_index_c2, val_index_c3, remainder_capacity], message


def main():

    # indexes, messages = compute_index(324.76)
    # print(indexes)
    print(find_best_capacity_value(5.7391304347826082e-11))


if __name__ == '__main__':
    main()

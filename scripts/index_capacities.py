# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Conversion between index value and capacities."""

from copy import deepcopy
import itertools

from scripts.utils import add_inverse, convert_decimal_to_binary


class IndexCapacityTransormation:

    def __init__(self, capacity_list):
        """

        Parameters
        ----------
        capacity_list: tuple
            Tuple of available capacities, ordered from smallest to largest.
        """
        self.capacity_list = capacity_list

        self.capacity_dict = dict()

        for i in range(len(capacity_list)):
            self.capacity_dict[i] = capacity_list[i]

    def index_to_capacity(self, index):
        """Convert the index to a capacity value.

        Parameters
        ----------
        index: int

        Returns
        -------
        capacity: int
        """
        circ = convert_decimal_to_binary(index)
        capacity = 0
        cap_index = 0
        for i in circ[::-1]:
            capacity += int(i) * self.capacity_list[cap_index]
            cap_index += 1

        return capacity

    def capacity_to_index(self, capacity, return_remainder=False):
        """Convert capacity to an index value.

        Parameters
        ----------
        capacity: int
            Capacity value to be transformed into indexes.
        return_remainder: bool
            Flag indicating whether to return the remainder capacity or not.
            Defaults to False.


        Returns
        -------
        index: int
            The index for the capacity box.
        capacity: float, int
            The remainder capacity
        """
        capacity_list = list(deepcopy(self.capacity_list))
        capacity_list.reverse()
        index = ''

        for capacity_value in capacity_list:
            if capacity >= capacity_value:
                # 'Add' from the left
                index = '1' + index
                capacity -= capacity_value
            else:
                index = '0' + index

        if return_remainder:
            return index
        else:
            return index, capacity

    def compute_all_possible_combinations(self):
        pass

    def get_all_possible_index_combinations(self):
        permutation_list = list()
        possible_values = (['0', '0', '0', '0', '0', '0'],
                           ['0', '0', '0', '0', '0', '1'],
                           ['0', '0', '0', '0', '1', '1'],
                           ['0', '0', '0', '1', '1', '1'],
                           ['0', '0', '1', '1', '1', '1'],
                           ['0', '1', '1', '1', '1', '1'],
                           ['1', '1', '1', '1', '1', '1'],
                           )
        for values in possible_values:
            perm = itertools.permutations(values)
            for val in perm:
                if val not in permutation_list:
                    permutation_list.append(val)

        return permutation_list


index_c1 = IndexCapacityTransormation(capacity_list=[20, 44, 94, 200, 440, 940])
index_c2 = IndexCapacityTransormation(capacity_list=[0.44, 0.94, 2, 4.4, 9.40])
index_c3 = IndexCapacityTransormation(capacity_list=[0.044, 0.066, 0.094, 0.200])


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
        cbox1 = index_c1.index_to_capacity(int(c1)) + index_c2.index_to_capacity(int(c2))
    elif serial == 1:
        cbox1 = add_inverse(index_c1.index_to_capacity(int(c1)), index_c2.index_to_capacity(int(c2)))
    else:
        cbox1 = None

    cbox2 = index_c3.index_to_capacity(c3)

    if cbox2 == 0:
        return cbox1 * 1e-9
    elif cbox1 == 0:
        return cbox2 * 1e-9
    else:
        return add_inverse(cbox1 * 1e-9, cbox2 * 1e-9)


def compute_total_capacity(c1, c2, c3, serial=0):
    if serial == 0:
        c_total = add_inverse(c1 + c2, c3)
    else:
        c_total = add_inverse(add_inverse(c1, c2), c3)
    return c_total


def compute_all_possible_capacities():
    capacity_values = list()
    for val_c1 in index_c1.capacity_list:
        for val_c2 in index_c2.capacity_list:
            for val_c3 in index_c3.capacity_list:
                for serial in [0, 1]:
                    capacity_values.append(compute_total_capacity(val_c1, val_c2, val_c3, serial=serial))

    return capacity_values



def compute_index(capacity):

    val_index_c1, remainder_capacity = index_c1.capacity_to_index(capacity)
    val_index_c2, remainder_capacity = index_c2.capacity_to_index(remainder_capacity)
    val_index_c3, remainder_capacity = index_c3.capacity_to_index(remainder_capacity)

    indexes_message = f'The indexes are as follows:\n' \
                      f'From the C1box: {val_index_c1}\n' \
                      f'From the C2box: {val_index_c2}\n' \
                      f'From the C3box: {val_index_c3}'
    capacity_error_message = f'The capacity error is:{remainder_capacity}'

    return [val_index_c1, val_index_c2, val_index_c3, remainder_capacity], [indexes_message, capacity_error_message]


def main():
    # compute_index(324.76)
    # print(compute_all_possible_capacities())
    print(index_c1.get_all_possible_index_combinations())


if __name__ == '__main__':
    main()

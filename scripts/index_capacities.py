# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Conversion between index value and capacities."""

from copy import deepcopy

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

    def capacity_to_index(self, capacity):
        """Convert capacity to an index value.

        Parameters
        ----------
        capacity: int

        Returns
        -------
        index: int
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

        return index


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


def main():
    print(index_c1.index_to_capacity(10))
    print(index_c1.capacity_to_index(65))


if __name__ == '__main__':
    main()

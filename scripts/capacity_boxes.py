# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Conversion between index value and capacities class."""


from copy import deepcopy

from scripts.parameters import capacity_box_1_list, capacity_box_2_list, capacity_box_3_list
from scripts.utils import convert_decimal_to_binary, convert_binary_to_decimal


class CapacityBoxes:
    """Class that converts between capacity boxes index and capacities."""

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

    def capacity_to_index(self, capacity, return_remainder=True, decimal='True'):
        """Convert capacity to an index value.

        Parameters
        ----------
        capacity: int
            Capacity value to be transformed into indexes.
        return_remainder: bool
            Flag indicating whether to return the remainder capacity or not.
            Defaults to False.
        decimal: bool
            Flag indicating whether to return the index as decimal or binary.
            Defaults to True.

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
        capacity_list = [i*10**-9 for i in capacity_list[:]]

        for capacity_value in capacity_list:
            if capacity >= capacity_value:
                # 'Add' from the left
                index = '1' + index
                capacity -= capacity_value
            else:
                index = '0' + index

        if decimal:
            index = convert_binary_to_decimal(index)

        if return_remainder:
            return index, capacity
        else:
            return index

    @property
    def max_index(self):
        """Return the maximum possible index as int from the length of the capacity list.

        As the indexes are in binary, the maximum is just (2 ** n - 1).

        Returns
        -------
        out: int
        """
        return int(2 ** len(self.capacity_list) - 1)


# Define the capacity boxes.
capacity_box_1 = CapacityBoxes(capacity_list=capacity_box_1_list)
capacity_box_2 = CapacityBoxes(capacity_list=capacity_box_2_list)
capacity_box_3 = CapacityBoxes(capacity_list=capacity_box_3_list)

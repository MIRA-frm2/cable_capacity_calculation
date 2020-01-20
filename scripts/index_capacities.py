# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Conversion between index value and capacities."""

from copy import deepcopy

from scripts.utils import add_inverse, convert_decimal_to_binary, convert_binary_to_decimal, \
    read_capacities_data_from_file, save_capacities_data_to_file


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
        return int(2 ** len(self.capacity_list) - 1)

    # def compute_all_possible_combinations(self):
    #     for index in range(int(2 ** len(self.capacity_list))):
    #         print(self.index_to_capacity(index))

    # def get_all_possible_index_combinations(self):
    #     permutation_list = list()
    #     possible_values = (['0', '0', '0', '0', '0', '0'],
    #                        ['0', '0', '0', '0', '0', '1'],
    #                        ['0', '0', '0', '0', '1', '1'],
    #                        ['0', '0', '0', '1', '1', '1'],
    #                        ['0', '0', '1', '1', '1', '1'],
    #                        ['0', '1', '1', '1', '1', '1'],
    #                        ['1', '1', '1', '1', '1', '1'],
    #                        )
    #     for values in possible_values:
    #         perm = itertools.permutations(values)
    #         for val in perm:
    #             if val not in permutation_list:
    #                 permutation_list.append(val)
    #
    #     return permutation_list


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

    data = dict()

    for val_c1 in range(index_c1.max_index):
        for val_c2 in range(index_c2.max_index):
            for val_c3 in range(index_c3.max_index):
                for serial in [0, 1]:
                    data[compute_capacity(val_c1, val_c2, val_c3, serial=serial)] = (val_c1, val_c2, val_c3, serial)

    save_capacities_data_to_file(data, '../data/capacities.csv')


def find_best_capacity_value(desired_capacity):
    values = read_capacities_data_from_file('data/capacities.csv')

    best_capacity = 0
    error = desired_capacity

    for i in range(len(values[0])):
        value = values[0][i]
        new_error = abs(value - desired_capacity)

        if new_error < error:
            best_capacity = value
            error = new_error

            connection_data = values[1][i], values[2][i], values[3][i], values[4][i]

    return best_capacity, error, connection_data


def compute_index(capacity, from_data_table=True):

    if from_data_table:
        best_capacity, remainder_capacity, connection_data = find_best_capacity_value(capacity)
        val_index_c1, val_index_c2, val_index_c3, connection_type = connection_data
    else:
        val_index_c1, remainder_capacity = index_c1.capacity_to_index(capacity)
        val_index_c2, remainder_capacity = index_c2.capacity_to_index(remainder_capacity)
        val_index_c3, remainder_capacity = index_c3.capacity_to_index(remainder_capacity)
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

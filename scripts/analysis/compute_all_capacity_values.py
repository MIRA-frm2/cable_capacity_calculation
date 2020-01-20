# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Compute all the capacities values allowed by the experimental setup."""


from scripts.capacity_boxes import capacity_box_1, capacity_box_2, capacity_box_3
from scripts.compute_values.capacities import compute_capacity
from scripts.utils import save_capacities_data_to_file


def compute_all_possible_capacities():
    """Compute all the experimental possible capacities from the values at hand."""
    data = dict()

    for val_c1 in range(capacity_box_1.max_index):
        for val_c2 in range(capacity_box_2.max_index):
            for val_c3 in range(capacity_box_3.max_index):
                for serial in [0, 1]:
                    data[compute_capacity(val_c1, val_c2, val_c3, serial=serial)] = (val_c1, val_c2, val_c3, serial)

    save_capacities_data_to_file(data, '../../data/capacities.csv')


if __name__ == '__main__':
    compute_all_possible_capacities()

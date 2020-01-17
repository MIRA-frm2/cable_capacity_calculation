# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Conversion from eigenfrequency to indexes of the capacity boxes."""

from scripts.optimize import compute_capacity_for_given_eigenfrequency
from scripts.index_capacities import compute_index
from scripts.parameters import computed_params


def main(eigenfrequency_value):

    capacity = compute_capacity_for_given_eigenfrequency(eigenfrequency_value, computed_params)
    numerical_values, messages = compute_index(capacity)

    print(messages[0])
    print(messages[1])


if __name__ == '__main__':
    frequency_value = 200000

    main(frequency_value)

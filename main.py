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
    print(f'For the given eigenfrequency of {eigenfrequency_value}, the desired capacity is: {capacity}\n')
    numerical_values, message = compute_index(capacity)

    print(message)

    hrf = 3.8/143000*eigenfrequency_value
    print(f'hrf = {str(hrf)}')

    return numerical_values, message


if __name__ == '__main__':
    frequency_value = int(input('welche frequenz?'))

    main(frequency_value)

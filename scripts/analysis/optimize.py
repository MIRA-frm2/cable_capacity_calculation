# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Empirical optimization of the relation between the eigenfrequency and the capacity.."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

from scripts.compute_values.capacities import compute_capacity_values
from scripts.compute_values.eigenfrequency_capacity import compute_eigen_frequency, \
    compute_capacity_for_given_eigenfrequency
from scripts.utils import read_data_from_file


def plot_main(capacity_values, theoretical_frequency, measured_frequency, optimized_values):
    """Plot the frequency values vs the capacities.

    Parameters
    ----------
    capacity_values: ndarray
        X axis consisting of the capacity values.
    theoretical_frequency: ndarray
        Frequency values computed using the eigenfrequency simple equation.
    measured_frequency: ndarray
        Measured frequency values.
    optimized_values: ndarray
        Frequency values computed using the optimized eigenfrequency equation.
    """
    plt.plot(capacity_values, theoretical_frequency, 'o')
    plt.plot(capacity_values, measured_frequency, 'v')
    plt.plot(capacity_values, optimized_values, '*')

    plt.xlabel('Capacity [mF]')
    plt.ylabel('Frequency [au]')

    plt.xscale('log')
    plt.yscale('log')

    plt.legend(['Theoretical frequency values', 'Measured frequency values', 'Optimized frequency values'],
               loc='best')

    plt.show()


def find_optimized_equation():
    """Find the parameters for the eigenfrequency equation."""

    # Read data from file
    measured_frequency, capacity_1, capacity_2, connection_type = read_data_from_file('../../data/data.csv')

    # Compute capacity values
    capacity_values = compute_capacity_values(capacity_1, capacity_2, connection_type)

    # Compute theoretical frequency
    theoretical_frequency = compute_eigen_frequency(np.asarray(capacity_values))

    # Optimize the theoretical equation
    params, params_covariance = optimize.curve_fit(compute_eigen_frequency, capacity_values, measured_frequency,
                                                   p0=[1, 1/2, 0, 0])
    optimized_values = compute_eigen_frequency(capacity_values, *params)

    # Plot the result
    plot_main(capacity_values, theoretical_frequency, measured_frequency, optimized_values)

    return params


def main(value):
    """Compute the capacity given an eigenfrequency.

    Parameters
    ----------
    value: float
        Eigenfrequency value.

    """
    computed_params = find_optimized_equation()
    result = compute_capacity_for_given_eigenfrequency(value, computed_params)
    print(result)


if __name__ == '__main__':
    # main(0.1)
    print(find_optimized_equation())

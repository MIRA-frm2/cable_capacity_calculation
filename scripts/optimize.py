# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Computation script for capacities and Eigenfrequencies."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

from scripts.index_capacities import compute_capacity
from scripts.utils import read_data_from_file

inductance = 22.45e-6  # [H]


def compute_eigen_frequency(circuit_capacity, a=1, n=1 / 2, b=0, d=0):
    """Compute the eigenfrequency.

    Parameters
    ----------
    circuit_capacity: float, ndarray
        Capacity of the elements in the circuit.
    a: float
        Prefactor/Amplitude.
    n: float
        Power law dependence.
    b: float
        X axis off set.
    d: float
        Y axis off set.

    Returns
    -------
    out: float, ndarray
        Eigenfrequency of the circuit taking into account the cable capacity.
    """
    prefactor = 1 / (2 * np.pi * np.sqrt(inductance))
    return prefactor * a * (np.asarray(circuit_capacity + b) ** (-n)) + d


def compute_capacity_for_given_eigenfrequency(eigenfrequency, params):
    """

    Parameters
    ----------
    eigenfrequency: float
        Frequency to be have the capacity computed at.
    params: tuple
        Tuple of parameters used for the eigenfrequency computation.

    Returns
    -------
    capacity: float
        Computed capacity needed for the given eigenfrequency.
    """
    a, n, b, d = params
    capacity = ((eigenfrequency - d) * (2 * np.pi * np.sqrt(inductance)) / a) ** n - b
    return capacity


def parasitic_capacity_calculation(capacity, effective_frequency, connection_type='serial'):
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
    measured_frequency, capacity_1, capacity_2, connection_type = read_data_from_file('data/data.csv')

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

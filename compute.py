#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:25:06 2020

@author: henrik
"""

import csv
import numpy as np
# import itertools as it
import matplotlib.pyplot as plt
from scipy import optimize

inductance = 2.15e-5


def read_data_from_file(file_name):
    """Read data from file.

    Parameters
    ----------
    file_name: str
        Name of the file to be read from.
    """
    _frequency = list()
    _capacity_1 = list()
    _capacity_2 = list()
    connection_type = list()

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if row[1] and row[2] and row[3]:
                if line_count == 0:
                    # print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    try:
                        _frequency.append(float(row[0]))
                        _capacity_1.append(float(row[1]))
                        _capacity_2.append(float(row[2]))

                        connection_type.append(int(row[3]))
                    except IndexError:
                        print("wtf")

        return np.asarray(_frequency), np.asarray(_capacity_1), np.asarray(_capacity_2), np.asarray(connection_type)


def add_inverse(a, b):
    """Adds two values as a parallel connection.

    Parameters
    ----------
    a: float, ndarray
    b: float, ndarray

    Returns
    -------
    out: float
        the inverse of the sum of their inverses
    """
    if a and b:
        return (a**(-1) + b**(-1))**(-1)
    else:
        return 0


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
    out: float
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


def index_to_c1(c1):
    """

    Parameters
    ----------
    c1

    Returns
    -------

    """
    circ = bin(c1)[2:]
    cap_list = [20, 44, 94, 200, 440, 940]
    cap_tot = 0
    cap_index = 0
    for i in circ[::-1]:
        cap_tot += int(i)*cap_list[cap_index]
        cap_index += 1
    
    return cap_tot


def index_to_c2(c2):
    """

    Parameters
    ----------
    c2

    Returns
    -------

    """
    circ = bin(c2)[2:]
    cap_list = [0.44, 0.94, 2, 4.4, 9.40]
    cap_tot = 0
    cap_index = 0
    for i in circ[::-1]:
        cap_tot += int(i)*cap_list[cap_index]
        cap_index += 1
    
    return cap_tot


def index_to_c3(c3):
    """

    Parameters
    ----------
    c3

    Returns
    -------

    """
    circ = bin(c3)[2:]
    cap_list = [0.044, 0.066, 0.094, 0.200]
    cap_tot = 0
    cap_index = 0
    for i in circ[::-1]:
        cap_tot += int(i)*cap_list[cap_index]
        cap_index += 1
    
    return cap_tot


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
        capacity_values.append(compute_capacity(capacity_1[i], capacity_2[i], 0, connection_type[i]))
    return np.asarray(capacity_values)


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
        cbox1 = index_to_c1(int(c1)) + index_to_c2(int(c2))
    elif serial == 1:
        cbox1 = add_inverse(index_to_c1(int(c1)), index_to_c2(int(c2)))
    else:
        cbox1 = None

    cbox2 = index_to_c3(c3)
    
    if cbox2 == 0:
        return cbox1*1e-9
    elif cbox1 == 0:
        return cbox2*1e-9
    else:
        return add_inverse(cbox1 * 1e-9, cbox2 * 1e-9)


def plot_main(capacity_values, theoretical_frequency, measured_frequency, optimized_values):
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
    # computed_params = find_optimized_equation()
    computed_params = [1.64910419e+00,  4.72453831e-01,  1.42870768e-10, -1.14410061e+04]
    result = compute_capacity_for_given_eigenfrequency(value, computed_params)
    print(result)


if __name__ == '__main__':
    main(0.1)
    # find_optimized_equation()

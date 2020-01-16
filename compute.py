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

                        connection_type.append(bool(row[3]))
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


def eigen_frequency(circuit_capacity, cable_capacity=0):
    """Compute the eigenfrequency.

    Parameters
    ----------
    circuit_capacity: float, ndarray
        Capacity of the elements in the circuit.
    cable_capacity: float, ndarray
        Cable capacity.

    Returns
    -------
    out: float
        Eigenfrequency of the circuit taking into account the cable capacity.
    """
    # if circuit_capacity == 0:
    #     return 0

    return 1 / (2 * np.pi * np.sqrt(inductance * np.asarray(circuit_capacity + cable_capacity)))


def parasitic_capacity_calculation(capacity, efective_frequency, connection_type='serial'):
    capacity_theo = (2 * np.pi * efective_frequency) ** -2 / inductance
    if connection_type == 'serial':
        return  capacity_theo - capacity
    else:
        return capacity_theo * capacity / (capacity - capacity_theo)


def index_to_c1(c1):
    circ = bin(c1)[2:]
    cap_list = [20, 44, 94, 200, 440, 940]
    cap_tot = 0
    cap_index = 0
    for i in circ[::-1]:
        cap_tot += int(i)*cap_list[cap_index]
        cap_index += 1
    
    return cap_tot


def index_to_c2(c2):
    circ = bin(c2)[2:]
    cap_list = [0.44, 0.94, 2, 4.4, 9.40]
    cap_tot = 0
    cap_index = 0
    for i in circ[::-1]:
        cap_tot += int(i)*cap_list[cap_index]
        cap_index += 1
    
    return cap_tot


def index_to_c3(c3):
    circ = bin(c3)[2:]
    cap_list = [0.044, 0.066, 0.094, 0.200]
    cap_tot = 0
    cap_index = 0
    for i in circ[::-1]:
        cap_tot += int(i)*cap_list[cap_index]
        cap_index += 1
    
    return cap_tot


def compute_capacity(c1, c2, c3=0, serial=0):
    if serial == 0:
        cbox1 = index_to_c1(int(c1)) + index_to_c2(int(c2))
    elif serial == 1:
        cbox1 = add_inverse(index_to_c1(int(c1)), index_to_c2(int(c2)))
    else:
        cbox1 = None

    cbox2 = index_to_c3(c3)
    
    if cbox2 == 0:
        return cbox1*1e-9
    if cbox1 == 0:
        return cbox2*1e-9
    else:
        return add_inverse(cbox1 * 1e-9, cbox2 * 1e-9)


def plot_capacity(frequency, c_par):
    plt.plot(frequency, c_par, '*')

    plt.xlabel('Frequency [au]')
    plt.ylabel('Capacity [mF]')

    plt.show()


def plot_capacities(frequency, c_par, c_ser):
    plt.plot(frequency, c_par)
    plt.plot(frequency, c_ser)

    plt.legend(['Parallel calculation', 'Serial calculation'])
    plt.xlabel('Frequency [au]')
    plt.ylabel('Capacity [mF]')

    plt.show()


def plot_frequencies(measured_frequency, theoretical_frequency):
    plt.plot(measured_frequency, theoretical_frequency, '*')

    plt.xlabel('Measured frequency [au]')
    plt.ylabel('Theoretical frequency [au]')

    plt.show()


def main():

    # liste = list(it.product(range(64), range(32), range(16)))

    measured_frequency, capacity_1, capacity_2, connection_type = read_data_from_file('data/data.csv')

    # c_par = add_inverse(np.asarray(capacity_1), np.asarray(capacity_2))
    # c_ser = np.asarray(capacity_1) + np.asarray(capacity_2)
    # plot_capacities(measured_frequency, c_par, c_ser)

    capacity_values = []
    for i in range(len(capacity_1)):
        capacity_values.append(compute_capacity(capacity_1[i], capacity_2[i], 0, connection_type[i]))

    # plot_capacity(measured_frequency, capacity_values)
    #
    # zeros = np.zeros(len(capacity_1))
    # theoretical_frequency = eigen_frequency(np.asarray(capacity_values), zeros)

    # plot_frequencies(measured_frequency, theoretical_frequency)

    result = parasitic_capacity_calculation(capacity_values, measured_frequency, connection_type='parallel')
    plot_capacity(measured_frequency, result)


if __name__ == '__main__':
    main()

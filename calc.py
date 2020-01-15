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

        return _frequency, _capacity_1, _capacity_2


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
    return (a**(-1) + b**(-1))**(-1)


def eigen_frequency(circuit_capacity, cable_capacity=0):
    """Compute the eigenfrequency.

    Parameters
    ----------
    circuit_capacity: float
        Capacity of the elements in the circuit.
    cable_capacity: float
        Cable capacity.

    Returns
    -------
    out: float
        Eigenfrequency of the circuit taking into account the cable capacity.
    """
    if circuit_capacity == 0:
        return 0

    inductance = 2.15e-5

    return 1 / (2 * np.pi * np.sqrt(inductance * (circuit_capacity + cable_capacity)))


def parallel_capacity_calculation(inductance, _capacity, ef):
    return (2*np.pi*ef) ** -2 / inductance - _capacity


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


def capacity(c1, c2, c3=0, serial=0):
    if serial == 0:
        cbox1 = index_to_c1(c1) + index_to_c2(c2)
    elif serial == 1:
        cbox1 = add_inverse(index_to_c1(c1), index_to_c2(c2))
    else:
        cbox1 = None

    cbox2 = index_to_c3(c3)
    
    if cbox2 == 0:
        return cbox1*1e-9
    if cbox1 == 0:
        return cbox2*1e-9
    else:
        return add_inverse(cbox1 * 1e-9, cbox2 * 1e-9)


def plot(frequency, c_par, c_ser):
    plt.plot(frequency, c_par)
    plt.plot(frequency, c_ser)

    plt.legend(['Parallel calculation', 'Serial calculation'])
    plt.xlabel('Frequency [a.u]')
    plt.ylabel('Capacity [mF]')

    plt.show()


def main():

    # liste = list(it.product(range(64), range(32), range(16)))

    frequency, capacity_1, capacity_2 = read_data_from_file('data.csv')

    c_par = add_inverse(np.asarray(capacity_1), np.asarray(capacity_2))
    c_ser = np.asarray(capacity_1) + np.asarray(capacity_2)

    plot(frequency, c_par, c_ser)

    # Legacy: '20 Jan 15
    # C0_list = []
    # C0_list = parCcalc(2.15e-5, line[1]*1e-9, line[0]))

    # C0_list = np.array(C0_list)
    #
    # plt.plot(freqtable1[:,0], C0_list/freqtable1[:,1])
    # cap_vs_ef = []
    # caps = []
    #
    # for el in liste:
    #    caps.append([el[0], el[1],el[2],capacity(el[0], el[1], el[2])])
    #
    # for cap in caps:
    #    cap_vs_ef.append([cap, efreq(cap[1])])
    #
    # cap_vs_ef = np.array(cap_vs_ef)
    # np.savetxt("table_caps", caps)


if __name__ == '__main__':
    main()

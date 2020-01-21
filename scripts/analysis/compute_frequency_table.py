# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Computation of the frequency table."""

import csv
from copy import deepcopy

from scripts.analysis.find_best_capacity_index import compute_index
from scripts.compute_values.eigenfrequency_capacity import compute_capacity_for_given_eigenfrequency
from scripts.utils import transform_frequency
from scripts.parameters import h_planck_constant, length, mass_neutron, n_digits, wavelength


def save_data_to_file(data, file_name, extension='.csv'):
    """Save data to file."""
    if extension in file_name:
        full_filename = file_name
    else:
        full_filename = f'{file_name}{extension}'

    with open(full_filename, 'w') as file:

        csv_writer = csv.writer(file, delimiter=',')
        csv_writer.writerow(["capacity", "c1_box_index", "c2_box_index", "c3_box_index", "connection_type"])

        for capacity, connection_data in data.items():
            row = list((capacity, connection_data[0], connection_data[1], connection_data[2], connection_data[3]))

            csv_writer.writerow(row)


def compute_frequency2_from_frequency1(frequency1):
    """Compute the second frequency from the first one.

    Parameters
    ----------
    frequency1: int, float

    Returns
    -------
    frequency2: int, float
    """
    prefactor = 1.2
    return prefactor * frequency1


def chopping_frequency(frequency1, frequency2):
    """Compute the chopping frequency

    Parameters
    ----------
    frequency1: int, float
    frequency2: int, float

    Returns
    -------
    out: int, float
    """
    return 2 * (frequency2 - frequency1)


def timebin(chopping_frequency_value):
    """Compute the timebin based on the chopping frequency.

    Parameters
    ----------
    chopping_frequency_value: int, float

    Returns
    -------
    out: int, float
    """
    number_of_periods = 16
    return number_of_periods * chopping_frequency_value


def mieze_time(chopping_frequency_value):
    """Compute the mieze time."""
    return ((mass_neutron/h_planck_constant) ** 2) * (wavelength ** 3) * chopping_frequency_value * length


def main():
    """Generate the frequency table."""

    with open('../../data/generated_table_data.csv', mode='w') as generated_table_data:
        table_data_writer = csv.writer(generated_table_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        table_data_writer.writerow(
            ['echotime',
             'cbox1_coil1_c1',
             'cbox1_coil1_c1c2serial',
             'cbox1_coil1_c2',
             'cbox1_coil1_c3',
             'cbox1_coil1_transformer',
             'cbox1_coil2_c1',
             'cbox1_coil2_c1c2serial',
             'cbox1_coil2_c2',
             'cbox1_coil2_c3',
             'cbox1_coil2_transformer',
             'cbox1_diplexer',
             'cbox1_fg_freq',
             'cbox1_power_divider',
             'cbox1_reg_amp',
             'cbox2_coil1_c1',
             'cbox2_coil1_c1c2serial',
             'cbox2_coil1_c2',
             'cbox2_coil1_c3',
             'cbox2_coil1_transformer',
             'cbox2_coil2_c1',
             'cbox2_coil2_c1c2serial',
             'cbox2_coil2_c2',
             'cbox2_coil2_c3',
             'cbox2_coil2_transformer',
             'cbox2_diplexer',
             'cbox2_fg_freq',
             'cbox2_power_divider',
             'cbox2_reg_amp',
             'hrf1',
             'hrf2',
             'hsf1',
             'hsf2',
             'psd_chop_freq',
             'psd_timebin_freq',
             'sf1',
             'sf2'])

        cbox1_coil1_transformer = 0
        cbox1_coil2_c1 = 0
        cbox1_coil2_c1c2serial = 0
        cbox1_coil2_c2 = 0
        cbox1_coil2_c3 = 0
        cbox1_coil2_transformer = 0
        cbox1_diplexer = 0
        cbox1_power_divider = 0
        cbox1_reg_amp = 1.6
        cbox2_coil1_transformer = 0
        cbox2_coil2_c1 = 0
        cbox2_coil2_c1c2serial = 0
        cbox2_coil2_c2 = 0
        cbox2_coil2_c3 = 0
        cbox2_coil2_transformer = 0
        cbox2_diplexer = 0
        cbox2_power_divider = 0
        cbox2_reg_amp = 1.6
        hsf1 = 0.4
        hsf2 = 0.4
        sf1 = 1.1
        sf2 = 1.1

        frequency1 = 30000

        while frequency1 < 1000000:
            print(frequency1)
            capacity = compute_capacity_for_given_eigenfrequency(frequency1)
            numerical_values, message = compute_index(capacity)
            val_index_c1_1, val_index_c2_1, val_index_c3_1, connection_type_1, remainder_capacity_1 = numerical_values

            print(f'{val_index_c1_1}, {val_index_c2_1}, {val_index_c3_1} {connection_type_1}')

            frequency2 = compute_frequency2_from_frequency1(frequency1)
            capacity = compute_capacity_for_given_eigenfrequency(frequency2)
            numerical_values, message = compute_index(capacity)
            val_index_c1_2, val_index_c2_2, val_index_c3_2, connection_type_2, remainder_capacity_2 = numerical_values

            print(f'{val_index_c1_2}, {val_index_c2_2}, {val_index_c3_2} {connection_type_2}')

            chopping_frequency_value = chopping_frequency(frequency1, frequency2)
            timebin_value = timebin(chopping_frequency_value)
            mieze_time_value = mieze_time(chopping_frequency_value)
            hrf1 = transform_frequency(frequency1)
            hrf2 = transform_frequency(frequency2)

            print(f'echo time: {mieze_time_value}')

            table_data_writer.writerow(
                [round(mieze_time_value*100000000, 3),
                 val_index_c1_1,
                 connection_type_1,
                 val_index_c2_1,
                 val_index_c3_1,
                 cbox1_coil1_transformer,
                 cbox1_coil2_c1,
                 cbox1_coil2_c1c2serial,
                 cbox1_coil2_c2,
                 cbox1_coil2_c3,
                 cbox1_coil2_transformer,
                 cbox1_diplexer,
                 round(frequency1, n_digits),
                 cbox1_power_divider,
                 cbox1_reg_amp,
                 val_index_c1_2,
                 connection_type_2,
                 val_index_c2_2,
                 val_index_c3_2,
                 cbox2_coil1_transformer,
                 cbox2_coil2_c1,
                 cbox2_coil2_c1c2serial,
                 cbox2_coil2_c2,
                 cbox2_coil2_c3,
                 cbox2_coil2_transformer,
                 cbox2_diplexer,
                 round(frequency2, n_digits),
                 cbox2_power_divider,
                 cbox2_reg_amp,
                 hrf1,
                 hrf2,
                 hsf1,
                 hsf2,
                 round(chopping_frequency_value, n_digits),
                 round(timebin_value, n_digits),
                 sf1,
                 sf2])

            # Assign the second frequency to the first one for the while loop
            frequency1 = deepcopy(frequency2)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""File storing the parameters from the computing the capacity indexes."""

# These values are obtained by running the optimization script.
computed_params = [1.68514381e+00, 4.72453838e-01, 1.42870779e-10, -1.14410010e+04]

# These values are taken from the datasheet for the capacity boxes.
capacity_box_1_list = [20, 44, 94, 200, 440, 940]
capacity_box_2_list = [0.44, 0.94, 2, 4.4, 9.40]
capacity_box_3_list = [0.044, 0.066, 0.094, 0.200]

inductance = 22.45e-6  # [H]
mass_neutron = 1.674927471e-27  # [kg]
h_planck_constant = 6.62607004e-34  # [m2 kg / s]
wavelength = 4.3e-10  # [m]
length = 193  # [?]

# Number of digits after comma to be rounded after
n_digits = 0

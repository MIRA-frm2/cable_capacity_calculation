# -*- coding: utf-8 -*-
#
# This file is part of MIEZE simulation.
# Copyright (C) 2019, 2020 TUM FRM2 E21 Research Group.
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Transformation equations between eigenfrequency and capacity."""

import numpy as np

from scripts.parameters import inductance


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
    capacity = ((eigenfrequency - d) * (2 * np.pi * np.sqrt(inductance)) / a) ** (-1/n) - b
    return capacity

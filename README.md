Cable Capacities Computation
============================

## About

This project computes the eigenfrequencies of the circuit taking into consideration the capacities of the cables 
themeslves.


## Documentation

### Main
In practice, one inputs in the [main program](main.py) the desired eigenfrequency and gets the required indexes for the capacity bocex..


### Optimize the frequency-capacity relation

The theoretical relation between the eigenfrequency of a LC circuit and the capacity is of the following form:

<img src="https://render.githubusercontent.com/render/math?math=f_{eigen}(C) = \dfrac{1}{2\pi \sqrt{L}}\dfrac{1}{\sqrt{C}}">

This relation is further generalized as:

<img src="https://render.githubusercontent.com/render/math?math=\dfrac{1}{\sqrt{C}} = C^{-\frac{1}{2}} \approx a ( C \perp b)^{-n} \perp d">

Based on experimentally measured values from [frequency table](data/freq_table_editted.ods), the values for the free 
parameters a, b, d are optimized to match the measured points and can be found in the [parameters file](scripts/parameters.py).
This functional relationship can be used to  efficiently extrapolate to other unmeasured points as well.

In practice, one inputs the desired eigenfrequency and gets the required capacity.

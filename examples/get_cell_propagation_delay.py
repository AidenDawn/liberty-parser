"""
Determine the propagation delay of a combinational cell.

1) Load the liberty file.
2) Load the correct timing table based on the cell name, output pin name and timing type.
3) Interpolate the timing table.
"""

from liberty.parser import parse_liberty
from liberty.types import *
import scipy.interpolate  # For interpolation.
import numpy as np

liberty_file = '../test_data/gscl45nm.lib'
library = parse_liberty(open(liberty_file).read())

# Get the time unit used in this library.
# Unfortunately liberty is not consistent with the format for units...
time_unit_str = library['time_unit'].value
cap_unit_str = library['capacitive_load_unit']

# Notice that different formats are used for both units.
print(f"time_unit_str = {time_unit_str}")
print(f"cap_unit_str = {cap_unit_str}")

# For simplicity the time units are hardcoded. Actually they would need
# to be derived from the extracted strings.
assert time_unit_str == '1ns'
time_unit = 1e-9
assert cap_unit_str == [1.0, 'pf']
cap_unit = 1e-12

cell_name = 'INVX1'
input_pin = 'A'
output_pin = 'Y'
input_rise_time = 1.0e-9  # 1 ns
output_load = 1e-12  # 1 pF

# Well get the delay for a rising edge.
timing_table_name = 'cell_rise'  # Use 'cell_fall' for falling edges.

# Find cell by name.
cell = select_cell(library, cell_name)
# Find the output pin by name.
pin = select_pin(cell, output_pin)

# Get the correct timing table.
timing_table = select_timing_table(pin, related_pin=input_pin,
                                   table_name=timing_table_name)

# Get indices and table data as numpy arrays.
x_axis = timing_table.get_array('index_1')
y_axis = timing_table.get_array('index_2')
data = timing_table.get_array('values')

# Find out which index is the output load and which the input slew.
template_name = timing_table.args[0]
template = library.get_group('lu_table_template', template_name)

x_label = template['variable_1']
y_label = template['variable_2']

indices = {
    x_label: x_axis,
    y_label: y_axis
}

assert 'total_output_net_capacitance' in indices
assert 'input_net_transition' in indices

# Get the correct indices and convert the units into SI units (Farads and seconds).
capacitance_index = indices['total_output_net_capacitance'] * cap_unit
input_transition_index = indices['input_net_transition'] * time_unit

# Now we have all the data ready and can find the delay by interpolation.

interp = scipy.interpolate.interp2d(capacitance_index,
                                    input_transition_index,
                                    data)

# Interpolate. (Will not do any extrapolation if the input is out of the specified table!)
propagation_delay = interp(output_load, input_rise_time)
propagation_delay = propagation_delay[0]  # Because interp returns an array.

# Find the validity ranges of the table.
cap_min = np.min(capacitance_index)
cap_max = np.max(capacitance_index)

slew_min = np.min(input_transition_index)
slew_max = np.max(input_transition_index)

if not cap_min <= output_load <= cap_max:
    print("Warning: output load is out of range.")

if not slew_min <= input_rise_time <= slew_max:
    print("Warning: input rise time is out of range.")

# Print the result.
print(f"Propagation delay from {input_pin} to {output_pin} of cell {cell_name} is "
      f"{propagation_delay} [{time_unit_str}].")

'''
USUSLS Simulator
Simulation Configuration file to be inputted into the system.
Author: Michael Ko
'''

test_config = [
    {
        "Component_name" : "NLS_position_calc",
    },
]

'''
Global Configurations
'''

from collections import namedtuple
Position = namedtuple('Position', 'x y z')

speed_of_sound = 1500 #m/s
hydrophone_positions = [
    Position(0, 0, 0),
    Position(2e-3, 0, 0),
    Position(0, 2e-3, 0),
    Position(0, 0, 2e-3),
    Position(1e-3, 1e-3, 1e-3),
]
'''
USUSLS Simulator
Simulation Configuration file to be inputted into the system.
Author: Michael Ko
'''

test_config = [
    {
        "Component_name" : "butterworth_filter",
        "Order" : "1",
        "Pole_positions" : ["one", "two", "three"]
    },

    {
        "Component_name" : "cross_correlator",
        "Order" : "2",
        "Pole_positions" : ["four", "five", "six"]
    }
]
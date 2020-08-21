'''
USUSLS Simulator
Module containing all classes and instances used.
Each class will auto-generate its parameters using the sim_config dictionary.
Author: Michael Ko
'''

class butterworth_filter:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

class cross_correlator:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])
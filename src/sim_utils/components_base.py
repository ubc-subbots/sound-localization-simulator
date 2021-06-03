'''
USUSLS Simulator
Module referencing the component name to it's relative file path in the system.
Author: Michael Ko
'''
'''
class butterworth_filter:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

class cross_correlator:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])
'''
'''
test_config = [
    {
        "butterworth_filter" : "test1"
        "Path" : "src/components/TDOA_position_calculation"
    },

    {
        "Component_name" : "cross_correlator",
        "Path" : "src/components/time_difference_calculations"
    }
]
'''

database = {
    "NLS_position_calc" : 'components.position_calc.NLS_position_calc',
    "cross_correlator" : ["test2", 'src/components/time_difference_calculations/test2.py']
}
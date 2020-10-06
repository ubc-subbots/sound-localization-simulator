'''
Author: Michael Ko
Purpose: Test file used to evalute input parser, will be deleted after implementation.
'''

class butterworth_filter:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])
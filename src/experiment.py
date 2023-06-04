import jsonpickle
import os

class Experiment:

    # Execute here
    def apply(self):
        raise NotImplementedError()

    def display_results(self):
        raise NotImplementedError

    # Write to file
    def dump(self):
        frozen = jsonpickle.encode(self)  # A json string
        dir_path = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def load(cls):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        

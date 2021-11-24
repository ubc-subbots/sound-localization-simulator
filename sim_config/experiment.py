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
        with open(dir_path + f'/../output/{self.__class__.__name__}.json', 'w') as f:
            f.write(frozen)

    @classmethod
    def load(cls):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            with open(dir_path + f'/../output/{cls.__name__}.json', 'r') as f:
                defrosted = jsonpickle.decode(f.read())  # type: Experiment
                defrosted.__init__()
                return defrosted
        except FileNotFoundError:
            return None

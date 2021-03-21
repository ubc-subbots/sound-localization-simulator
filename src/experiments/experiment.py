import jsonpickle


class Experiment:

    # Execute here
    def apply(self):
        raise NotImplementedError()

    def display_results(self):
        raise NotImplementedError

    # Write to file
    def dump(self):
        frozen = jsonpickle.encode(self)  # A json string
        with open(f'{self.__class__.__name__}.json', 'w') as f:
            f.write(frozen)

    @classmethod
    def load(cls):
        try:
            with open(f'{cls.__name__}.json', 'r') as f:
                defrosted = jsonpickle.decode(f.read())  # type: Experiment
                return defrosted
        except FileNotFoundError:
            return None

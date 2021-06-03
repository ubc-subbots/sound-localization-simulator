import importlib


class Chain():

    def __init__(self, chain_start_data):
        self.chain = []
        self.chain_start_data = chain_start_data
        self.frames = []

    def add_component(self, component):
        self.chain.append(component)

    def __repr__(self):
        print([ele.__repr__() for ele in self.chain])

    def apply(self):
        prev_signal = self.chain_start_data
        for component_instance in self.chain:

            curr_signal = prev_signal

            # Instantiate the class (pass arguments to the constructor, if needed)
            result = component_instance.apply(curr_signal)
            frame = component_instance.write_frame(None)

            self.frames.append(frame)

            prev_signal = result

        # Do something with result
        return prev_signal

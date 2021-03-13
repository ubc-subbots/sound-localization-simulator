from sim_utils.input_generation import InputGeneration
import global_vars
import numpy as np

class InputGenerationStage:
    
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

        # as many channels as there are hydrophones
        self.num_components = len(global_vars.hydrophone_positions)

        self.components = [
            self.create_component(i, initial_data)
            for i in range(self.num_components)
        ]

    def apply(self, sim_signal):
        return tuple(
            component.apply(sim_signal)
            for component in self.components
        )

    def write_frame(self, frame):
        pass
    
    def create_component(self, component_index, stage_initial_data):
        initial_data = stage_initial_data
        # adjust component name to indicate channel
        initial_data["id"] = "Input Generation [" + str(component_index) + "]"

        # add hydrophone position based on component index
        initial_data["hydrophone_position"] = global_vars.hydrophone_positions[component_index]

        return InputGeneration(initial_data)
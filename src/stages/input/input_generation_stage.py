from sim_utils.input_generation import InputGeneration
import global_vars
import numpy as np


class InputGenerationStage:
    
    def __init__(self, measurement_period, duty_cycle):
        # as many channels as there are hydrophones
        self.num_components = len(global_vars.hydrophone_positions)

        # Create InputGeneration
        self.components = []
        # add hydrophone position based on component index
        for i in range(self.num_components):
            hydrophone_position = global_vars.hydrophone_positions[i]
            self.components.append(
                InputGeneration(hydrophone_position, measurement_period, duty_cycle)
            )

    def apply(self, sim_signal):
        return tuple(
            component.apply(sim_signal)
            for component in self.components
        )

    def write_frame(self, frame):
        pass
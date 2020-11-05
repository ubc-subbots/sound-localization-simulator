from components.sampling.ideal_adc import ideal_adc
from simulator_main import sim_config as cfg
import numpy as np

class ideal_adc_stage:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

        # always using hydrophone 0 as reference
        self.num_components = len(cfg.hydrophone_positions)

        self.components = [
            self.create_component(i, initial_data)
            for i in range(self.num_components)
        ]

    def apply(self, sim_signal):
        return [
            np.array(component.apply(sig))
            for (component, sig) in zip(self.components, sim_signal)
        ]

    def write_frame(self, frame):
        pass

    def create_component(self, component_index, stage_initial_data):
        initial_data = stage_initial_data
        initial_data["id"] = "Ideal ADC [" + str(component_index) + "]"

        return ideal_adc(initial_data)
from components.sampling.ideal_adc import IdealADC
import global_vars
import numpy as np

class IdealADCStage:
    '''
    stage to simulate an ADC for every hydrophone signal channel
    '''

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
            np.array(component.apply(sig))
            for (component, sig) in zip(self.components, sim_signal)
        )

    def write_frame(self, frame):
        pass

    def create_component(self, component_index, stage_initial_data):
        initial_data = stage_initial_data
        initial_data["id"] = "Ideal ADC [" + str(component_index) + "]"

        return IdealADC(initial_data)
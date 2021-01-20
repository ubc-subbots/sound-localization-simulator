from simulator_main import sim_config as cfg
from components.tdoa.cross_correlation import CrossCorrelation
import numpy as np
import matplotlib.pyplot as plt

class CrossCorrelationStage:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

        # always using hydrophone 0 as reference
        self.num_components = len(cfg.hydrophone_positions) - 1

        self.components = [
            self.create_component(i, initial_data)
            for i in range(self.num_components)
        ]

    def apply(self, sim_signal):
        plt.figure()
        i=0
        for signal in sim_signal:
           plt.plot(signal, label="hydrophone %0d"%i)
           i += 1
        plt.legend()

        phase_analysis_inputs = [
            (sim_signal[0], sim_signal[i+1])
            for i in range(self.num_components)
        ]

        tdoa =  tuple(
            component.apply(input_sig)
            for (component, input_sig) in zip(self.components, phase_analysis_inputs)
        )

        print("calculated time differences:", tdoa)

        return tdoa

    def write_frame(self, frame):
        pass
    
    def create_component(self, component_index, stage_initial_data):
        initial_data = stage_initial_data
        initial_data["id"] = self.id + "[%0d]"%(component_index+1)

        return CrossCorrelation(initial_data)
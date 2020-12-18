from simulator_main import sim_config as cfg
from components.sampling.threshold_index_finder import ThresholdIndexFinder

class ThresholdCaptureTrigger:

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

        self.num_components = len(cfg.hydrophone_positions)

        self.components = [
            self.create_component(i, initial_data)
            for i in range(self.num_components)
        ]

    def apply(self, sim_signal):
        trigger_indices = [
            component.apply(signal)
            for component, signal in zip(self.components, sim_signal)
        ]

        trigger_index = min(trigger_indices)

        print(trigger_index, self.num_samples)

        return tuple(
            signal[trigger_index:(trigger_index + self.num_samples)]
            for signal in sim_signal
        )

    def write_frame(self, frame):
        pass

    def create_component(self, component_index, stage_initial_data):
        initial_data = stage_initial_data
        initial_data["id"] = "Threshold Time Finder [" + str(component_index) + "]"

        return ThresholdIndexFinder(initial_data)
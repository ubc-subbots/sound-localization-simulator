from simulator_main import sim_config as cfg
from components.sampling.threshold_index_finder import ThresholdIndexFinder

class ThresholdCaptureTrigger:
    '''
    captures a certain segment of the signal based on the specified threshold.
    Note that this appears after signal quantization (so signal range is between
    -2^(num_bits-1) and 2^(num_bits-1)).

    This emulates the fact that our system can only grab a portion of the signal.
    '''

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

        # instantiate a threshold time finder for each component
        self.num_components = len(cfg.hydrophone_positions)

        self.components = [
            self.create_component(i, initial_data)
            for i in range(self.num_components)
        ]

    def apply(self, sim_signal):
        # find the point at which the signals cross the treshold
        trigger_indices = [
            component.apply(signal)
            for component, signal in zip(self.components, sim_signal)
        ]

        # trigger based on the first signal that crosses the threshold
        trigger_index = min(trigger_indices)

        # capture a window after the trigger as the analyzed signal
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
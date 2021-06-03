import global_vars
from components.sampling.threshold_index_finder import ThresholdIndexFinder


class ThresholdCaptureTrigger:
    '''
    captures a certain segment of the signal based on the specified threshold.
    Note that this appears after signal quantization (so signal range is between
    -2^(num_bits-1) and 2^(num_bits-1)).

    This emulates the fact that our system can only grab a portion of the signal.
    '''

    def __init__(self, num_samples, threshold):
        self.num_samples = num_samples
        self.threshold = num_samples

        # instantiate a threshold time finder for each component
        self.num_components = len(global_vars.hydrophone_positions)

        # Create ThresholdIndexFinder
        self.components = []
        for i in range(self.num_components):
            self.components.append(
                ThresholdIndexFinder(num_samples, threshold)
            )

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
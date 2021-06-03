import numpy as np
import global_vars

class PhaseAnalysis:
    
    def __init__(self, identifier):
        self.identifier = identifier

    def apply(self, sim_signal):
        hydrophone0_phase = get_phase(sim_signal[0])
        hydrophone_phase = get_phase(sim_signal[1])

        return (hydrophone0_phase - hydrophone_phase) / (2 * np.pi * global_vars.signal_frequency)

    def write_frame(self, frame):
        return {}


# I can likely get this without a sampling frequency, but that is a todo:
def get_phase(input_signal):
    fft = np.fft.fft(input_signal)

    # fft generates a lot of values that are not 0 due to floating point error
    # eg 3.15e-15 + 3.15e-15j. However these values create notable phase angles
    # These should just be set to 0
    threshold = max(np.abs(fft)) / 10000
    indices_below_thresh = abs(fft) < threshold
    fft[indices_below_thresh] = 0
    
    # this fixes scaling, I'm not 100% sure why this is needed
    fft = 2 * fft / global_vars.sampling_frequency

    # find index that matches to signal frequency in the fft spectrum
    sig_discrete_frequency = global_vars.signal_frequency / global_vars.sampling_frequency # fft spectrum ranges from discrete:[0, 1] -> continuous[0, Fs]
    fft_index =  int(round(sig_discrete_frequency*len(fft), 0))

    return np.angle(fft[fft_index])
import numpy as np


# I can likely get this without a sampling frequency, but that is a todo:
def get_phase(input_signal, sampling_frequency):
    fft = np.fft(input_signal)

    # fft generates a lot of values that are not 0 due to floating point error
    # eg 3.15e-15 + 3.15e-15j. However these values create notable phase angles
    # These should just be set to 0
    threshold = max(np.abs(fft)) / 10000
    indices_below_thresh = abs(fft) < threshold
    fft[indices_below_thresh] = 0
    # this fixes scaling, I'm not 100% sure why this is needed
    fft = 2 * fft / sampling_frequency

    return np.angle(fft)

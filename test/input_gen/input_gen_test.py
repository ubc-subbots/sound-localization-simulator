from hypothesis import given
import hypothesis.strategies as st

import sim_utils.input_generation as ig
import numpy as np
import math
import matplotlib.pyplot as plt

input_generation = ig.InputGeneration({"measurement_period" : 0.5, "duty_cycle": 0.1})


@given(st.integers(min_value=100, max_value=100000),
     st.floats(min_value=0.1, max_value=3, allow_nan=False, allow_infinity=False),
     st.floats(min_value=0.1, max_value=100000, allow_nan=False, allow_infinity=False),
     st.floats(min_value=0.1, allow_nan=False, allow_infinity=False)
)
def test_sines_are_correct_length(sampling_rate, measurement_period, sine_wave_freq, phase_time):
    sine_wave = input_generation._sine_wave(sampling_rate, sine_wave_freq, measurement_period, phase_time)
    assert len(sine_wave) == math.floor(sampling_rate * measurement_period)

@given(st.integers(min_value=100, max_value=100000),
     st.floats(min_value=1, max_value=3, allow_nan=False, allow_infinity=False),
     st.floats(min_value=2, max_value=100000, allow_nan=False, allow_infinity=False),
     st.floats(min_value=0.1, allow_nan=False, allow_infinity=False)
     )
def sines_have_correct_fft(sampling_rate, measurement_period, sine_wave_freq, phase_time):
    sine_wave = input_generation._sine_wave(sampling_rate, sine_wave_freq, measurement_period, phase_time)
    dt = 1/sampling_rate
    fft = np.fft.fft(sine_wave) * dt
    freqs = np.fft.fftfreq(len(sine_wave)) * sampling_rate
    index = np.argmax(abs(fft))

    small_acceptance_criteria = sine_wave_freq - 0.5 < abs(freqs[index]) < sine_wave_freq + 0.5
    big_acceptance_criteria = sine_wave_freq * 0.95 < abs(freqs[index]) < sine_wave_freq * 1.05
    assert small_acceptance_criteria or big_acceptance_criteria

# sines_have_correct_fft()
# test_sines_are_correct_length()

plt.plot(input_generation.apply(None)[0])
plt.show()
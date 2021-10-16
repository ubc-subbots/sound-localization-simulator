from stages.tdoa.music import get_autocorrelation_matrix, generate_delay_vector, calculate_music_coefficient
import numpy as np
from numpy import linalg as la
from scipy.fft import fft
import matplotlib.pyplot as plt

f = 1/(2*np.pi)
delay_fraction = 3
tau = 1/(delay_fraction*f)
num_samples = 1000
num_cycles = 5

t = np.linspace(0, num_cycles/f, num_samples)
y1 = np.sin(2*np.pi*f*t)
y2 = np.sin(2*np.pi*f*(t+tau))
y3 = np.sin(2*np.pi*f*(t+2*tau))

plt.figure()
plt.plot(t, y1, label="y1")
plt.plot(t, y2, label="y2")
plt.plot(t, y3, label="y3")
plt.title("Test Signals")
plt.legend()

Y = [y1, y2, y3]
Y = np.array([fft(sig) for sig in Y])

sampling_frequency = f * (num_samples/num_cycles)
f_vals = np.linspace(-sampling_frequency/2, sampling_frequency/2, num_samples)
plt.figure()
plt.plot(f_vals, np.angle(Y[0]), label="y1")
plt.plot(f_vals, np.angle(Y[1]), label="y2")
plt.plot(f_vals, np.angle(Y[2]), label="y3")
plt.title("Fourier Phase")
plt.legend()

Y = get_autocorrelation_matrix(Y)
w, v = la.eig(Y)

# remove eigenvector associated with largest eigenvalue
b_vectors = [v[i] for i in range(len(v)) if i != np.argmax(w)]

tau_vals = np.linspace(0, 1/(2*f), 20)
j_music = []
for tau_val in tau_vals:
    # create delay array
    delay_vector = generate_delay_vector(tau_val, 3, f)

    # calculate MUSIC coefficient
    j_music.append(calculate_music_coefficient(b_vectors, delay_vector))

plt.figure()
plt.plot(tau_vals, j_music)
plt.title("J_MUSIC vs delay value")
plt.show()
from sim_utils.common_types import CONV_2_DEG, CartesianPosition, CylindricalPosition
from stages.tdoa.music import generate_steering_vector, get_autocorrelation_matrix, calculate_music_coefficient, plane_wave_prop_delay
import numpy as np
from numpy import linalg as la
from scipy.fft import fft
import matplotlib.pyplot as plt
import global_vars

f = 1
delay_fraction = 3
tau = 1/(delay_fraction*f)
num_samples = 1000
num_cycles = 5

global_vars.hydrophone_positions = [
    CartesianPosition(0,0,0),
    CartesianPosition(1,0,0),
    CartesianPosition(2,0,0)
    # CartesianPosition(-1,0,0),
    # CartesianPosition(-2,0,0)
]

global_vars.signal_frequency = 1

t = np.linspace(0, num_cycles/f, num_samples)
y1 = np.cos(2*np.pi*f*t)
y2 = np.cos(2*np.pi*f*(t-tau))
y3 = np.cos(2*np.pi*f*(t-2*tau))
# y4 = np.cos(2*np.pi*f*(t+tau))
# y5 = np.cos(2*np.pi*f*(t+2*tau))

plt.figure()
plt.plot(t, y1, label="y1")
plt.plot(t, y2, label="y2")
plt.plot(t, y3, label="y3")
# plt.plot(t, y4, label="y4")
# plt.plot(t, y5, label="y5")
plt.title("Test Signals")
plt.legend()

# Y = [y1, y2, y3, y4, y5]
Y = [y1, y2, y3]
Y = np.array([fft(sig)/num_samples for sig in Y])

sampling_frequency = f * (num_samples/num_cycles)
global_vars.sampling_frequency = sampling_frequency
f_vals = np.linspace(0, sampling_frequency, num_samples)
plt.figure()
plt.plot(f_vals, np.real(Y[0]), label="y1")
plt.plot(f_vals, np.real(Y[1]), label="y2")
plt.plot(f_vals, np.real(Y[2]), label="y3")
# plt.plot(f_vals, np.real(Y[3]), label="y4")
# plt.plot(f_vals, np.real(Y[4]), label="y5")
plt.title("Fourier Real")
plt.legend()

plt.figure()
plt.plot(f_vals, np.imag(Y[0]), label="y1")
plt.plot(f_vals, np.imag(Y[1]), label="y2")
plt.plot(f_vals, np.imag(Y[2]), label="y3")
# plt.plot(f_vals, np.imag(Y[3]), label="y4")
# plt.plot(f_vals, np.imag(Y[4]), label="y5")
plt.title("Fourier Imag")
plt.legend()


Y = get_autocorrelation_matrix(Y, is_fft=True)
print("Matrix")
print(Y)
w, v = la.eig(Y)
print("eig")
print(w)
print(v)

# remove eigenvector associated with largest eigenvalue
b_vectors = [v[i] for i in range(len(v)) if i != np.argmax(w)]

# just conforming to function signature
def delay_func(pos, tau, dummy2):
    return pos.x*tau

tau_vals = np.linspace(0, 1/(2*f), 20)
j_music = []
for tau in tau_vals:
    # create delay array
    steering_vector = generate_steering_vector(delay_func, tau)

    print("tau=%f"%tau)
    print("angle", np.angle(steering_vector)*CONV_2_DEG)

    # calculate MUSIC coefficient
    j_music.append(calculate_music_coefficient(b_vectors, steering_vector))

plt.figure()
plt.plot(tau_vals, j_music)
plt.title("J_MUSIC vs delay value")

global_vars.hydrophone_positions = [
    CartesianPosition(0,0,0),
    CartesianPosition(0.5,0,0),
    CartesianPosition(1,0,0)
    # CartesianPosition(-1,0,0),
    # CartesianPosition(-2,0,0)
]
global_vars.speed_of_sound = 1
global_vars.pinger_position = CylindricalPosition(10, np.pi/3, 0)

phi_vals = np.linspace(0, 2*np.pi, 20)
j_music = []
for phi in phi_vals:
    # create delay array
    steering_vector = generate_steering_vector(plane_wave_prop_delay, phi)

    print("phi=%f"%(phi*CONV_2_DEG))
    print("angle", np.angle(steering_vector)*CONV_2_DEG)

    # calculate MUSIC coefficient
    j_music.append(calculate_music_coefficient(b_vectors, steering_vector))

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.plot(phi_vals, j_music)
plt.title("J_MUSIC vs polar angle")


plt.show()
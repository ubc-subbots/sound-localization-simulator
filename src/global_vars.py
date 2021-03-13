from sim_utils.common_types import *

##############################################
# Gloabl Parameters
##############################################

speed_of_sound = 1500 #m/s

#### position information ####
hydrophone_positions = [
    CylindricalPosition(0, 0, 0),
    CylindricalPosition(1.85e-2, 0, -1e-2),
    CylindricalPosition(1.85e-2, np.pi/2, -1e-2),
    CylindricalPosition(1.85e-2, np.pi, -1e-2),
    CylindricalPosition(1.85e-2, -np.pi/2, -1e-2),
]
pinger_position = CylindricalPosition(15, 0, 5)

#### frequency information ####
signal_frequency = 40e3
# used as ADC sampling frequency and for "digital" portion
sampling_frequency = 20*signal_frequency
# picked to be much higher so it's approximately continuous and can be used in "analog" portion
continuous_sampling_frequency = 100*signal_frequency
# TODO: double check pinger on-off frequency
carrier_frequency = 1

simulation_chain = [
    {
        "component_name"        : "InputGenerationStage",
        "id"                    : "Input Generation Stage",
        "measurement_period"    : 2,
        "duty_cycle"            : 0.05
    },
    {
        "component_name"        : "GaussianNoise",
        "id"                    : "Gaussian Noise",
        "mu"                    : 0,
        "sigma"                 : 0.01
    },
    {
        "component_name"        : "IdealADCStage",
        "id"                    : "ideal ADC stage",
        "num_bits"              : 12,
        "quantization_method"   : QuantizationType.midtread
    },
    {
        "component_name"        : "ThresholdCaptureTrigger",
        "id"                    : "Threshold Capture Trigger",
        "num_samples"           : int(10 * (sampling_frequency / signal_frequency)), # sample 10 cycles of the wave
        "threshold"             : 0.05*(2**11)
    },
    {
        "component_name"        : "CrossCorrelationStage",
        "id"                    : "Cross Correlation Stage",
    },
    {
        "component_name"        : "NLSPositionCalc",
        "id"                    : "NLS",
        "optimization_method"   : OptimizationType.nelder_mead,
        "initial_guess"         : PolarPosition(10, np.pi)
    }
]
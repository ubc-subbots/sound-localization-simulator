from components import position_calc
from stages.localization.localization_utils import nelder_mead
import global_vars
from stages.localization.multilateration import NLSPositionCalc
from sim_utils.common_types import PolarPosition, OptimizationType

class InitialPositionEstimator:
    '''
    Computes an initial position for the pinger
    '''

    def __init__(self, identifier = "Initial Position Estimator"):
        self.identifier = identifier

    def apply(self, sim_signal):
        nls = NLSPositionCalc(optimization_type=OptimizationType.nelder_mead)

        position_estimate = nls.apply(sim_signal)

        global_vars.initial_guess = PolarPosition(position_estimate.r, position_estimate.phi)

        return sim_signal

    def write_frame(self, frame):
        return frame

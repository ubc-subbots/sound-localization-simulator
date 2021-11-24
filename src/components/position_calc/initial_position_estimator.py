from components import position_calc
from components.position_calc.position_calc_utils import nelder_mead
import global_vars
from components.position_calc.nls_position_calc import NLSPositionCalc
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

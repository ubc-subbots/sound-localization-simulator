'''
USUSLS Simulator
Module referencing the component name to it's relative file path in the system.
Author: Michael Ko
'''

database = {
    "InputGeneration"       : "sim_utils.input_generation",
    "InputGenerationStage"  : "components.input.input_generation_stage",
    "IdealADC"              : "components.sampling.ideal_adc",
    "IdealADCStage"         : "components.sampling.ideal_adc_stage",
    "PhaseAnalysis"         : "components.tdoa.phase_analysis",
    "PhaseAnalysisStage"    : "components.tdoa.phase_analysis_stage",
    "NLSPositionCalc"       : "components.position_calc.nls_position_calc"
}
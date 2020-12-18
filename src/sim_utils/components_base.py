'''
USUSLS Simulator
Module referencing the component name to it's relative file path in the system.
Author: Michael Ko
'''

database = {
    "InputGeneration"           : "sim_utils.input_generation",
    "InputGenerationStage"      : "stages.input.input_generation_stage",
    "IdealADC"                  : "components.sampling.ideal_adc",
    "IdealADCStage"             : "stages.sampling.ideal_adc_stage",
    "ThresholdIndexFinder"      : "components.sampling.threshold_index_finder",
    "ThresholdCaptureTrigger"   : "stages.sampling.threshold_capture_trigger",
    "PhaseAnalysis"             : "components.tdoa.phase_analysis",
    "PhaseAnalysisStage"        : "stages.tdoa.phase_analysis_stage",
    "NLSPositionCalc"           : "components.position_calc.nls_position_calc"
}
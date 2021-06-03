# Component/Stage Database
This file contains documentation about the various components and stages used by the simulator. Each entry in this document is titled by the name of the component, and contains information about:
* Description of functionality
* Import path
* Required configuration parameters (specific to component)
* Global parameters used by the component/stage
* Required input signal format
* Output signal format

## InputGeneration
The inputGeneration component generates the signal detected by a single hydrophone for a given pinger position. The component accounts **ONLY** for the time difference across the signals, and does not deal with attenuation or noise. All hydrophones receive a signal with an amplitude of 1.

### Import Path
```python
from sim_utils.input_generation import InputGeneration
```

### Configuration Parameters

<table width="1000">
  <tr>
    <td> Parameter Name </td>
    <td> Description </td>
    <td> Expected Datatype </td>
    <td> Default Value </td>
    <td> Valid Range </td>
  </tr>
  <tr>
    <td> id </td>
    <td> Unique identifier for component instantiation. Used to distinguish between two instantiation of the same component. </td>
    <td> str </td>
    <td> N/A </td>
    <td> Could be any string value. Recommended to have something descriptive </td>
  </tr>
  <tr>
    <td> measurement_period </td>
    <td> The time range, in seconds, of the generated signal </td>
    <td> float </td>
    <td> N/A </td>
    <td> Could theoretically be any value, but recommended to be around a few cycles of the signal </td>
  </tr>
  <tr>
    <td> duty_cycle </td>
    <td> The percentage of time the signal is "on" for. The signal will be 0 for all "off" times and a sinusoid with amplitude 1 for "on" times </td>
    <td> float </td>
    <td> N/A </td>
    <td> A number between 0 (always off) and 1 (always on) </td>
  </tr>
  <tr>
    <td> hydrophone_index </td>
    <td> An index specifying which hydrophone will be used. For example, if index is 1, hydrophone 1 will be used and the position used in the component will be <code>cfg.hydrophone_positions[1]</code>  </td>
    <td> float </td>
    <td> N/A </td>
    <td> A number between 0 (always off) and 1 (always on) </td>
  </tr>
</table>

### Global Parameters Used
refer to the [Global Parameters](global_parameters.md) page for more information about each global parameters in the configuration.  
* hydrophone_positions
* pinger_position
* speed_of_sound
* continuous_sampling_frequency
* carrier_frequency
* signal_frequency

### Required Input Signal Format
No input signal is required for this component

### Output Signal Format
numpy array of shape (measurement_period*continuous_sampling_frequency,)
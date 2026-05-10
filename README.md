# SDRplay GNU Radio Examples

A collection of GNU Radio Companion flowgraphs and Python analysis tools for SDRplay RSP devices.

## Repository Structure
- **/flowgraphs**: `.grc` files for capturing and visualising IQ data. 
- **/analysis**: Python scripts for generating IQ density plots from recorded files.

## Getting Started
1. **Capture:** Open the flowgraphs in GNU Radio Companion. Use the sliders to tune to a signal and record the output to a file (e.g., `capture.iq`).
2. **Analyse:** Move your recorded file into the `/analysis` folder.
3. **Plot:** Run `python iq_density_plotter.py`. You can edit the `USER SETTINGS` at the top of the script to zoom in on specific modulations.

## License
MIT License

# SDRplay GNU Radio Examples

A collection of GNU Radio Companion flowgraphs and Python analysis tools for SDRplay RSP devices.

## Repository Structure
- **/flowgraphs**: `.grc` files for capturing and visualising IQ data. 
- **/analysis**: Python scripts for generating IQ density plots from recorded files.
- **/data**: The intended directory for your `.iq` recordings.

## Getting Started
1. **Capture:** Open a flowgraph in GNU Radio Companion. Use the sliders to tune to a signal and record the output. 
2. **Save:** Save your recording (e.g., `capture.iq`) into the **/data** folder.
3. **Plot:** Open a terminal in the **/analysis** folder and run `python iq_density_plotter.py`. 
4. **Customise:** You can edit the `USER SETTINGS` at the top of the script to change the filename or zoom in on specific modulations.

## License
MIT License

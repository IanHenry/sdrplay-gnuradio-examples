import numpy as np
import matplotlib.pyplot as plt
import os

# =============================================================================
# USER SETTINGS
# Modify these variables to change which file is loaded and how it is displayed.
# =============================================================================

# 1. The name of your IQ recording. 
# The script expects this file to be inside the '../data/' folder.
FILE_NAME = "capture.iq"   

# 2. Slice Settings: Choose which part of the recording to look at.
# For large files, plotting the whole thing can be slow and blurry.
START_SAMPLE = 0          # The index of the first sample to include
END_SAMPLE = 100000       # The index of the last sample to include

# 3. Hexbin Bounds: This defines the mathematical "box" for the density map.
# Increase this if your signal is very strong and clipping the edges.
PLOT_EXTENT = 0.8         

# 4. Visual Zoom: This controls the final display window on the I and Q axes.
# 0.1 is usually a good zoom for standard modulations.
ZOOM_LIMIT = 0.1          

# =============================================================================
# PATH SETUP
# This logic ensures the script finds your data regardless of your OS.
# =============================================================================

# Get the absolute path of the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level from the 'analysis' folder, then into the 'data' folder
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data", FILE_NAME)

# Check if the file actually exists before trying to load it
if not os.path.exists(DATA_PATH):
    print(f"ERROR: Could not find the file: {FILE_NAME}")
    print(f"Looking in: {DATA_PATH}")
    print("Ensure you have saved your GNU Radio capture into the 'data' folder.")
else:
    # =========================================================================
    # DATA PROCESSING
    # =========================================================================

    # Load the binary data. GNU Radio saves IQ as interleaved 32-bit floats.
    # NumPy's complex64 format maps these directly to I + jQ.
    data = np.fromfile(DATA_PATH, dtype=np.complex64)

    # Take the slice defined in the User Settings
    data_slice = data[START_SAMPLE:END_SAMPLE]

    # Split the complex samples into their Real (I) and Imaginary (Q) components
    I = data_slice.real
    Q = data_slice.imag

    # =========================================================================
    # PLOTTING
    # =========================================================================

    plt.figure(figsize=(9, 7))

    # 'hexbin' creates a 2D histogram using hexagonal bins.
    # gridsize: The number of hexagons across the plot (higher = more detail).
    # bins='log': Uses a logarithmic scale for the colour (crucial for SDR data).
    # extent: Sets the mathematical limits [xmin, xmax, ymin, ymax].
    hb = plt.hexbin(I, Q, gridsize=150, cmap='magma', bins='log',
                    extent=[-PLOT_EXTENT, PLOT_EXTENT, -PLOT_EXTENT, PLOT_EXTENT])
    
    # Add a colour bar to show the density scale
    plt.colorbar(hb, label='Log10 sample count per bin')
    
    # Apply visual zoom limits to focus on the constellation shape
    plt.xlim(-ZOOM_LIMIT, ZOOM_LIMIT)
    plt.ylim(-ZOOM_LIMIT, ZOOM_LIMIT)

    # Add titles and axis labels
    plt.title(f"IQ Density Map: {FILE_NAME}")
    plt.xlabel("In-phase (I)")
    plt.ylabel("Quadrature (Q)")
    
    # Ensure the plot is perfectly square so the constellation isn't distorted
    plt.axis('equal')
    plt.grid(alpha=0.3) # Add a subtle grid for reference
    
    print(f"Successfully plotting {END_SAMPLE - START_SAMPLE} samples from {FILE_NAME}")
    plt.show()

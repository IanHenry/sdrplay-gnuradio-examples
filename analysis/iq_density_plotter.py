import numpy as np
import matplotlib.pyplot as plt
import os

# --- USER SETTINGS ---
FILENAME = "capture.iq"   # Change this to your recorded file
START_SAMPLE = 0          # Start index of the slice
END_SAMPLE = 100000       # End index of the slice
PLOT_EXTENT = 0.5         # Broad bounds for the density calculation
ZOOM_LIMIT = 0.1          # Visual zoom for the I/Q axes
# ---------------------

if not os.path.exists(FILENAME):
    print(f"Error: {FILENAME} not found. Place your IQ file in this folder.")
else:
    data = np.fromfile(FILENAME, dtype=np.complex64)
    data_slice = data[START_SAMPLE:END_SAMPLE]
    I, Q = data_slice.real, data_slice.imag

    plt.figure(figsize=(9, 7))
    hb = plt.hexbin(I, Q, gridsize=150, cmap='magma', bins='log',
                    extent=[-PLOT_EXTENT, PLOT_EXTENT, -PLOT_EXTENT, PLOT_EXTENT])
    plt.colorbar(hb, label='Log10 count')
    plt.xlim(-ZOOM_LIMIT, ZOOM_LIMIT)
    plt.ylim(-ZOOM_LIMIT, ZOOM_LIMIT)
    plt.title(f"IQ Density Map: {FILENAME}")
    plt.axis('equal')
    plt.show()

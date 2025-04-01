#
# Test the matplotlib.pyplot library
#

import matplotlib.pyplot as plt
import numpy as np

# Create data
theta = np.linspace(0, 2 * np.pi, 100)
r = np.abs(np.sin(theta))

# Create the figure
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(6, 6))

# Plot the data
ax.plot(theta, r)

# Set fixed limits for the radial and angular axes
ax.set_ylim(0, 10)  # Radial limits
ax.set_theta_zero_location('N')  # Set the 0-degree line at the top (North)

# Display the plot
plt.show()

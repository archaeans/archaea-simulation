import numpy as np
import matplotlib.pyplot as plt

# Read vector field U
data_U = np.loadtxt("../../400/U", dtype=str, skiprows=23)
Ux = np.array([float(value[0]) for value in data_U])
Uy = np.array([float(value[1]) for value in data_U])
Uz = np.array([float(value[2][:-1]) for value in data_U])

# Read cell center coordinates C
data_C = np.loadtxt("../../400/C", skiprows=23)
Cx = data_C[:, 0]
Cy = data_C[:, 1]
Cz = data_C[:, 2]

# Plot the velocity magnitude on the plane
vel_magnitude = np.sqrt(Ux**2 + Uy**2 + Uz**2)
plt.scatter(Cx, Cy, c=vel_magnitude)
plt.colorbar(label='Velocity Magnitude')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Velocity Magnitude on Plane')

# Save the figure as PNG
plt.savefig('velocity_magnitude.png', dpi=300)

# Show the plot
plt.show()
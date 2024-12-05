import matplotlib.pyplot as plt
import numpy as np

def fit_func(x, y):
    return -(np.power(x, 2) + np.power(y, 2)) + 4

x = 4
y = -3.4
z = fit_func(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot single points
ax.scatter(x, y, z, color='red', s=50, label='Points')  # 's' controls the size of points

# Add labels
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('3D Scatter Plot')

# Add a legend
ax.legend()

# Show the plot
plt.show()
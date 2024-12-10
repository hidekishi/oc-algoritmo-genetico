import matplotlib.pyplot as plt
import numpy as np
import lib

population = np.array([])
x = 4
y = -3.4
z = lib.fitFunc(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, color='red', s=10, label='Points')

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('3D Scatter Plot')

ax.legend()
plt.show()
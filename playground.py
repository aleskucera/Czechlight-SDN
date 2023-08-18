import numpy as np
import matplotlib.pyplot as plt

# Example boolean array
boolean_array = np.array([True, False, True, False, True, False, False, True])

# Convert boolean array to integer (0s and 1s)
int_array = boolean_array.astype(int)

# Create a step plot
plt.step(np.arange(len(int_array)), int_array, where='mid')
plt.xlabel('Index')
plt.ylabel('Value (0 or 1)')
plt.title('Boolean Array Visualization')
plt.ylim(-0.1, 1.1)
plt.grid()
plt.show()

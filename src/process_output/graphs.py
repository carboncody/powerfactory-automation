import matplotlib.pyplot as plt
import numpy as np

# Example data (replace with your actual data)
positions_km = [10, 20, 30, 40, 50]  # Kilometers
power_kA = [2.5, 3.0, 2.8, 3.5, 2.2]  # Kiloamps

# Create a line plot
plt.plot(positions_km, power_kA, marker='o', label='Power (kA)')

# Add labels and title
plt.xlabel('Position (km)')
plt.ylabel('Power (kA)')
plt.title('Power vs. Position')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

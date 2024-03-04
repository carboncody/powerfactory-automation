import matplotlib.pyplot as plt
import os

def plot_busbar_voltages(data, name, output_path):
    os.makedirs(output_path, exist_ok=True)
    
    # Create a single plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Group data by timestamps
    grouped_data = {}
    for row in data:
        timestamp = row[4]  # Assuming timestamp is at index 4
        distance = float(row[2])  # Assuming distance is at index 2
        voltage = float(row[3])  # Assuming voltage is at index 3

        if timestamp not in grouped_data:
            grouped_data[timestamp] = {'distances': [], 'voltages': []}
        
        grouped_data[timestamp]['distances'].append(distance)
        grouped_data[timestamp]['voltages'].append(voltage)

    # Plot data for each timestamp
    for timestamp, vals in grouped_data.items():
        ax.plot(vals['distances'], vals['voltages'], label=timestamp, marker=".")

    ax.set_title("Busbar Voltage vs. Distance" + " - " + name)
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Voltage (V)")
    ax.legend()

    plt.tight_layout()

    plt.savefig(os.path.join(output_path, name + "-busbar_voltages.png"), dpi=300)
    plt.close()

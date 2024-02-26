import csv
import matplotlib.pyplot as plt
import os


def plot_busbar_currents(csv_path, output_dir="utils"):
    """
    Reads a CSV file containing busbar data and creates two line graphs:
    - One for type 'R' with current vs. distance.
    - One for type 'K' with current vs. distance.

    Args:
        csv_path: Path to the CSV file.
        output_dir (str, optional): Directory to save the plots. Defaults to "utils".
    """
    data = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            busbar_name, type_, distance, current = row
            data.append((busbar_name, type_, float(distance), float(current)))

    # Separate data by type
    type_r_data = [row for row in data if row[1] == "R"]
    type_k_data = [row for row in data if row[1] == "K"]

    # Create plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot type R data
    if type_r_data:
        distances_r = []
        currents_r = []
        for row in type_r_data:
            values = row[2:4]  # Extract only distance and current
            distances_r.append(float(values[0]))
            currents_r.append(float(values[1]))
        ax1.plot(distances_r, currents_r, label="Type R", marker="o")
        ax1.set_title("Busbar Current (Type R)")
        ax1.set_xlabel("Distance (km)")
        ax1.set_ylabel("Voltage (V)")
        ax1.legend()
    else:
        ax1.text(0.5, 0.5, "No data for type R", ha="center", va="center")

    # Plot type K data
    if type_k_data:
        distances_k = []
        currents_k = []
        for row in type_k_data:
            values = row[2:4]  # Extract only distance and current
            distances_k.append(float(values[0]))
            currents_k.append(float(values[1]))
        ax2.plot(distances_k, currents_k, label="Type K", marker="o")
        ax2.set_title("Busbar Current (Type K)")
        ax2.set_xlabel("Distance (km)")
        ax2.set_ylabel("Voltage (V)")
        ax2.legend()
    else:
        ax2.text(0.5, 0.5, "No data for type K", ha="center", va="center")

    # Auto-adjust axes (optional)
    plt.tight_layout()

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save plots with appropriate names
    plt.savefig(os.path.join(output_dir, "busbar_current_type_R.png"), dpi=300)
    plt.savefig(os.path.join(output_dir, "busbar_current_type_K.png"), dpi=300)

    # Close the plot window (optional)
    plt.close()


plot_busbar_currents("C:\\Users\\tempk\\Documents\\GitHub\\ris-sogm\\busbar_name_current_table.csv")

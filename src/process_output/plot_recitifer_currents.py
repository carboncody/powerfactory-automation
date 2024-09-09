import matplotlib.pyplot as plt
import os

def plot_recitifer_currents(data, output_path):
    # Rounding the current values to 2 decimal places
    data['current [A]'] = data['current [A]'].round(2)

    # Creating a directory to save the graphs if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Generating and saving the graphs
    for rectifier in data['rectifier_name'].unique():
        print(f"Creating current vs. time graph for recitifier {rectifier}...")
        rectifier_data = data[data['rectifier_name'] == rectifier]
        plt.figure()
        plt.plot(rectifier_data['timestamp [HH:MM:SS]'], rectifier_data['current [A]'], marker='o')
        plt.title(f'Current vs Time for {rectifier}')
        plt.xlabel('Timestamp [HH:MM:SS]')
        plt.xticks(rotation=45)
        plt.ylabel('Current [A]')
        plt.grid(True)
        plt.tight_layout()
        file_path = os.path.join(output_path, f'{rectifier}.png')
        plt.savefig(file_path)
        plt.close()
    
    colors = plt.cm.get_cmap('tab20', len(data['rectifier_name'].unique()))  # Colormap with enough distinct colors
    i = 0  # Initialize color index   

    plt.figure()
    for rectifier in data['rectifier_name'].unique():
        rectifier_data = data[data['rectifier_name'] == rectifier]
        plt.plot(rectifier_data['timestamp [HH:MM:SS]'], rectifier_data['current [A]'], marker='.', color=colors(i), label=rectifier)
        i += 1

    print("Creating current vs. time graph for all rectifiers...")
    plt.title('Current vs Time for All Rectifiers')
    plt.xlabel('Timestamp [HH:MM:SS]')
    plt.xticks(rotation=45)
    plt.ylabel('Current [A]')
    plt.grid(True)
    plt.tight_layout()

    # Adjust the legend placement
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    file_path = os.path.join(output_path, 'all_rectifiers.png')
    plt.savefig(file_path, bbox_inches='tight', dpi=400)
    plt.close()
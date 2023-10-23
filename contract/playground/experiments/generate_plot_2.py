import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.patches as mpatches


def generate_plot():
    # Read the data from the CSV file
    data = pd.read_csv("experiment_data_2.csv")

    # Separate the data into variables
    x_values = data["Iteration"].tolist()
    y_values = data["Function"].tolist()
    proposers = data["Proposer 1"].tolist()

    # Map colors and calculate percentages based on function and proposer combination
    colors = []
    part1_increment = 0
    part1_decrement = 0
    part2_increment = 0
    part2_decrement = 0

    for i in range(len(y_values)):
        if proposers[i] == "EMGUFI4UI3CF7VIKSAVFU65RLA6FAPSVU6TM4IZUYOVXSVR7HSZJGGOQUU":
            if y_values[i] == 0:
                colors.append("lime")  # bright green
                part1_increment += 1
            else:
                colors.append("cyan")  # bright cyan
                part1_decrement += 1
        else:
            if y_values[i] == 0:
                colors.append("magenta")  # bright magenta
                part2_increment += 1
            else:
                colors.append("yellow")  # bright yellow
                part2_decrement += 1

    total_part1 = part1_increment + part1_decrement
    total_part2 = part2_increment + part2_decrement

    lime_percentage = part1_increment / total_part1 * 100
    cyan_percentage = part1_decrement / total_part1 * 100
    magenta_percentage = part2_increment / total_part2 * 100
    yellow_percentage = part2_decrement / total_part2 * 100

    # Plot data
    plt.scatter(x_values, y_values, c=colors)

    # Set plot title and labels
    plt.title("Function Call Analysis Based on Proposer")
    plt.xlabel("Iterations")
    plt.ylabel("Functions Executed")

    # Define x-tick labels
    plt.yticks([0, 1], ["Decrement", "Increment"])

    ax = plt.gca()  # get the current axes
    ax.xaxis.set_major_locator(
        MaxNLocator(integer=True)
    )  # ensure x-axis values are integers

    # Create custom legend
    patches = [
        mpatches.Patch(
            color="lime", label=f"Increment (part1): {lime_percentage:.2f}%"
        ),
        mpatches.Patch(
            color="cyan", label=f"Decrement (part1): {cyan_percentage:.2f}%"
        ),
        mpatches.Patch(
            color="magenta", label=f"Increment (part2): {magenta_percentage:.2f}%"
        ),
        mpatches.Patch(
            color="yellow", label=f"Decrement (part2): {yellow_percentage:.2f}%"
        ),
    ]
    plt.legend(handles=patches, loc="best")

    plt.savefig("plot.svg", format="svg")
    plt.show()


if __name__ == "__main__":
    generate_plot()

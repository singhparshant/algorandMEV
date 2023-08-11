import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.patches as mpatches


def generate_plot():
    # Read the data from the CSV file
    data = pd.read_csv("experiment_data.csv")

    # Separate the data into x_values, y_values, colors and additional information
    x_values = data["Iteration"].tolist()
    y_values = data["Function"].tolist()
    colors = data["Color"].tolist()
    increment_count = data["Increment Count"].tolist()[
        0
    ]  # these values are same in every row, so just take the first one
    percentage_increment = data["Increment Percentage"].tolist()[0]
    decrement_count = data["Decrement Count"].tolist()[0]
    percentage_decrement = data["Decrement Percentage"].tolist()[0]

    # Generate the information string
    increment_info = f"Increment: {increment_count} times ({percentage_increment:.2f}%)"
    decrement_info = f"Decrement: {decrement_count} times ({percentage_decrement:.2f}%)"

    # Plot data
    scatter = plt.scatter(x_values, y_values, c=colors, cmap="bwr")

    # Set plot title and labels
    plt.title("Frequency of Increment and Decrement Functions")
    plt.xlabel("Iterations")
    plt.ylabel("Functions Executed")

    # Define x-tick labels and color bar
    plt.yticks([0, 1])

    ax = plt.gca()  # get the current axes
    ax.xaxis.set_major_locator(
        MaxNLocator(integer=True)
    )  # ensure the x-axis values are integers

    # Create custom legend
    red_patch = mpatches.Patch(color="red", label="Decrement(Purestake Node)")
    blue_patch = mpatches.Patch(color="blue", label="Increment(TUM Node)")
    plt.legend(handles=[red_patch, blue_patch])

    # Print the results on the plot
    plt.subplots_adjust(top=0.85)
    plt.figtext(0.3, 0.93, increment_info, fontsize=10, color="blue")
    plt.figtext(0.3, 0.9, decrement_info, fontsize=10, color="red")

    plt.savefig("plot.svg", format="svg")
    plt.show()


if __name__ == "__main__":
    generate_plot()

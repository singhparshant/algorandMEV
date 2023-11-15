import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.patches as mpatches


def generate_plot():
    # Read the data from the CSV file
    data = pd.read_csv("experiment_data_3.csv")

    # Separate the data into variables
    x_values = data["Iteration"].tolist()
    y_values = data["Function"].tolist()
    proposers = data["Proposer 1"].tolist()

    # Map colors and calculate percentages based on function and proposer combination
    colors = []
    part_counts = {
        part: {"increment": 0, "decrement": 0}
        for part in ["Alice", "Bob", "Thomas", "Alex"]
    }

    color_map = {
        "Alice": {"0": "lime", "1": "cyan"},
        "Bob": {"0": "magenta", "1": "yellow"},
        "Thomas": {"0": "blue", "1": "red"},
        "Alex": {"0": "green", "1": "orange"},
    }

    proposer_map = {
        "FJ4Z6WHDTIBSA72XNN55MUIUZQUYFFBKXTU4EDFAR5XR4R6CV5CR6DYEHU": "Alice",
        "NGVE57RDBABVTWYKUPBOVOHXZ2JHBVLOJXZNG2BVKQZTLGM7XH4VHLQP64": "Thomas",
        "PME5E5SOV33LLEYEZNNJAUAPMY6ZS4BBWQ432YG456OQVHZCFALCFEH7KU": "Bob",
        "SKV2WCTAYCA7YX2YIUH6WQBLNJ4JYMB6TNK737DIL5Z4N6LG52XXKXU4VM": "Alex",
    }

    for i in range(len(y_values)):
        part = proposer_map[proposers[i]]
        function = str(y_values[i])
        colors.append(color_map[part][function])

        if function == "0":
            part_counts[part]["increment"] += 1
        else:
            part_counts[part]["decrement"] += 1

    # Plot data
    plt.scatter(x_values, y_values, c=colors)

    # Set plot title and labels
    plt.title("Function Call Analysis Based on Proposer")
    plt.xlabel("Iterations")
    plt.ylabel("Functions Executed")

    # Define x-tick labels
    plt.yticks([0, 1], ["Decrement", "Increment"])

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Create custom legend
    patches = []
    for part, counts in part_counts.items():
        total = counts["increment"] + counts["decrement"]
        increment_percentage = counts["increment"] / total * 100
        decrement_percentage = counts["decrement"] / total * 100
        patches.extend(
            [
                mpatches.Patch(
                    color=color_map[part]["0"],
                    label=f"Increment ({part}): {increment_percentage:.2f}%",
                ),
                mpatches.Patch(
                    color=color_map[part]["1"],
                    label=f"Decrement ({part}): {decrement_percentage:.2f}%",
                ),
            ]
        )

    plt.legend(handles=patches, loc="best")

    plt.savefig("plot.svg", format="svg")
    plt.show()


if __name__ == "__main__":
    generate_plot()

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.patches as mpatches

def generate_plot():
    # Read the data from the CSV file
    data = pd.read_csv("experiment_data.csv")

    # Separate the data into variables
    x_values = data["Iteration"].tolist()
    y_values = data["Function"].tolist()
    proposers = data["Proposer 1"].tolist()

    # Setup to count the number of increments and decrements based on function and proposer combination
    part_counts = {
        part: {"increment": 0, "decrement": 0}
        for part in ["part1", "part2", "part3", "part4"]
    }

    proposer_map = {
        "FJ4Z6WHDTIBSA72XNN55MUIUZQUYFFBKXTU4EDFAR5XR4R6CV5CR6DYEHU": "part1",
        "NGVE57RDBABVTWYKUPBOVOHXZ2JHBVLOJXZNG2BVKQZTLGM7XH4VHLQP64": "part3",
        "PME5E5SOV33LLEYEZNNJAUAPMY6ZS4BBWQ432YG456OQVHZCFALCFEH7KU": "part2",
        "SKV2WCTAYCA7YX2YIUH6WQBLNJ4JYMB6TNK737DIL5Z4N6LG52XXKXU4VM": "part4",
    }

    for i in range(len(y_values)):
        part = proposer_map[proposers[i]]
        function = y_values[i]
        if function == 0:
            part_counts[part]["increment"] += 1
        else:
            part_counts[part]["decrement"] += 1

    # Print the count results
    for part, counts in part_counts.items():
        print(f"For {part}:")
        print(f"Increment function was called {counts['increment']} times.")
        print(f"Decrement function was called {counts['decrement']} times.")
        print("----------")

if __name__ == "__main__":
    generate_plot()

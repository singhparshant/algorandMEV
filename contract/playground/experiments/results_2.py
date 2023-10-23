import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv("experiment_data.csv")

# Define the proposers
proposer1 = "EMGUFI4UI3CF7VIKSAVFU65RLA6FAPSVU6TM4IZUYOVXSVR7HSZJGGOQUU"
proposer2 = "BFQYPRLMZJUL724E3AW65DSRZRHY2YHNKTXUQKPDRPU5BYSGOE2VQ46LNU"

# Filter the data based on the proposers
data_proposer1 = data[data["Proposer 1"] == proposer1]
data_proposer2 = data[data["Proposer 1"] == proposer2]

# For proposer1, calculate the counts of Increment (Function = 0) and Decrement (Function = 1)
increment_proposer1 = sum(data_proposer1["Function"] == 0)
decrement_proposer1 = sum(data_proposer1["Function"] == 1)

# For proposer2, calculate the counts of Increment (Function = 0) and Decrement (Function = 1)
increment_proposer2 = sum(data_proposer2["Function"] == 0)
decrement_proposer2 = sum(data_proposer2["Function"] == 1)

# Print the results
print(f"When {proposer1} is proposer: Increment called {increment_proposer1} times. Decrement called {decrement_proposer1} times.")
print(f"When {proposer2} is proposer: Increment called {increment_proposer2} times. Decrement called {decrement_proposer2} times.")

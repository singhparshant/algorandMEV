# Algorand MEV

This is the repo for running experiments on algorand to determine whether MEV is possible on algorand.

# Setup

## Install dependencies

```
cd contract
poetry shell
poetry install
```

## Build a contract

```
cd playground/counter
python build.py
```

## Generate data and plot

```
python generate_data.py // Change the number of iterations in the for loop
python plot.py
```

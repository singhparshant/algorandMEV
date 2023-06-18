from http import client
import algosdk
import pyteal as pt
import algokit_utils

# from beaker import Application, Authorize, GlobalStateValue, sandbox
# from beaker.client import ApplicationClient
from algosdk import mnemonic, account, transaction, atomic_transaction_composer, abi
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.v2client import algod
import os
from playground.experiments.utils import get_mainnet_indexer_client
from playground.experiments.utils import get_mainnet_algod_client
from playground.experiments.utils import get_testnet_indexer_client
from playground.experiments.utils import get_testnet_algod_client
from dotenv import load_dotenv
import json
import numpy as np
import statistics


load_dotenv()  # take environment variables from .env.


def mean_median():
    # client = get_mainnet_algod_client()
    client = get_mainnet_indexer_client()

    txns_per_block = []

    # For algod
    # last_round = client.status()["last-round"]

    # For indexer
    last_round = 29869684

    print("Last round: ", last_round)

    # iterate over the last 1000 blocks
    for round in range(last_round - 1000, last_round + 1):
        block_info = client.block_info(round)
        # print("Block info: ", json.dumps(block_info, indent=4)
        # When using the algod client, use this code:
        # if "txns" in block_info["block"]:
        #     num_transactions = len(block_info["block"]["txns"])
        # else:
        #     num_transactions = 0
        # When using the indexer, use this code instead:
        if "transactions" in block_info:
            num_transactions = len(block_info["transactions"])
        else:
            num_transactions = 0
        txns_per_block.append(num_transactions)

    # Now you can calculate and print the mean and median number of transactions
    mean = np.mean(txns_per_block)
    median = statistics.median(txns_per_block)

    print("Mean number of transactions: {0:.2f}".format(mean))
    print(f"Median number of transactions: {median}")


if __name__ == "__main__":
    mean_median()

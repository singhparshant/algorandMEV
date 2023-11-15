from textwrap import indent
import algosdk
import pyteal as pt
import algokit_utils
import json
from algosdk import mnemonic, account, transaction, atomic_transaction_composer, abi
from algosdk.v2client import algod
import concurrent.futures

import os
from playground.experiments.utils import get_mainnet_TUM_algod_client
from playground.experiments.utils import get_TUM_indexer_client
from playground.experiments.utils import get_mainnet_algod_client
from playground.experiments.utils import get_mainnet_indexer_client
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import random

load_dotenv()  # take environment variables from .env.

mnemonic_1 = os.getenv("MNEMONIC")
private_key = mnemonic.to_private_key(mnemonic_1)
account_address = account.address_from_private_key(private_key)

algod_indexer = get_TUM_indexer_client()
algod = get_mainnet_TUM_algod_client()

start_round = 1
# Get the latest block's round number
end_round = 0
try:
    status_info = algod.status()
    end_round = status_info.get("last-round")
except Exception as e:
    print(f"An error occurred while fetching the latest round: {e}")

print(f"End round: {end_round}")


def fetch_block_info(round_number):
    retries = 2  # Number of retries
    while retries > 0:
        try:
            block_info = algod_indexer.block_info(round_number)
            # print(json.dumps(block_info, indent=4))
            transactions = block_info.get("transactions", [])
            num_txns = len(transactions)

            print(f"Block {round_number} has {num_txns} transactions.")
            if num_txns > 2000:
                print(f"Block {round_number} has {num_txns} transactions.")
                with open("results.txt", "a") as f:
                    f.write(f"Block {round_number} has {num_txns} transactions.\n")

            break  # Exit the while loop if successful
        except Exception as e:
            print(f"An error occurred for block {round_number}: {e}")
            retries -= 1
            sleep_duration = 0.01 + random.uniform(0, 1)  # Adding some jitter
            sleep(sleep_duration)  # Sleep for 2+ seconds before retrying
        sleep_duration = 0.01
        sleep(sleep_duration)  # Sleep for 2+ seconds before retrying


# Use a ThreadPool to fetch blocks in parallel
with ThreadPoolExecutor(max_workers=1) as executor:  # Reduced number of workers
    executor.map(fetch_block_info, range(end_round - 2, end_round + 1))

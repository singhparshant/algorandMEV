import time
import algosdk
import pyteal as pt
import algokit_utils
import json
from algosdk import mnemonic, account, transaction, atomic_transaction_composer, abi
from algosdk.v2client import algod
from algosdk.atomic_transaction_composer import AccountTransactionSigner
import concurrent.futures
import msgpack
from beaker.client import ApplicationClient
from algosdk.atomic_transaction_composer import (
    ABIResult,
    AtomicTransactionComposer,
    TransactionSigner,
    TransactionWithSigner,
)
from concurrent.futures import ThreadPoolExecutor
import base64
import os
from playground.experiments.utils import (
    get_test_non_part_2,
    get_test_non_part_1,
)
from dotenv import load_dotenv
import csv

load_dotenv()  # take environment variables from .env.

# Initialize lists to track proposers and confirmed rounds
proposers_1 = []
proposers_2 = []
confirmed_rounds_1 = []
confirmed_rounds_2 = []


def generate_data():
    mnemonic_1 = "margin tackle shift airport stadium stool bounce step staff speak debate what resource era abuse evil draft answer tornado slide solid legend pond abstract crystal"
    private_key = mnemonic.to_private_key(mnemonic_1)
    app_id = 1001  # 238906986

    # Initialize counters for increment and decrement functions
    increment_count = 0
    decrement_count = 0

    # Initialize lists to store data for scatter plot
    x_values = []  # Function names
    y_values = []  # Frequency of each function
    colors = []  # Color of each point

    first_function = "None"
    color = ""

    client1 = get_test_non_part_1()
    # client1 = get_testnet_TUM_algod_client()
    client2 = get_test_non_part_2()
    # client2 = get_testnet_algod_client()

    with open("../last_executed/artifacts/contract.json") as f:
        js = f.read()
    contract = abi.Contract.from_json(js)

    for i in range(50):
        previous_value = print_global_state(client2, app_id)
        print("Previous Value:", previous_value)
        atc1 = AtomicTransactionComposer()
        atc2 = AtomicTransactionComposer()
        atc1.add_method_call(
            app_id=app_id,
            method=contract.get_method_by_name("decrement"),
            method_args=[],
            sp=client1.suggested_params(),
            sender=account.address_from_private_key(private_key),
            signer=AccountTransactionSigner(private_key),
        )

        atc2.add_method_call(
            app_id=app_id,
            method=contract.get_method_by_name("increment"),
            method_args=[],
            sp=client2.suggested_params(),
            sender=account.address_from_private_key(private_key),
            signer=AccountTransactionSigner(private_key),
        )

        # Using ThreadPoolExecutor to send transactions in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            result1 = executor.submit(submit_and_wait_for_conf, client1, atc1)
            result2 = executor.submit(submit_and_wait_for_conf, client2, atc2)

            txids1, transaction_info_1, confirmed_round_1, proposer_1 = result1.result()
            txids2, transaction_info_2, confirmed_round_2, proposer_2 = result2.result()

            print("txids for atc1: ", txids1)
            print("txids for atc2: ", txids2)
        #  Execute submit_atc directly for both atc1 and atc2
        # txids2 = submit_atc(atc2, client2)
        # txids1 = submit_atc(atc1, client1)

        # print("txids for atc1: ", txids1)
        # print("txids for atc2: ", txids2)

        # transaction_info_1, confirmed_round_1 = wait_for_confirmation(client1, txids1[0])
        # transaction_info_2, confirmed_round_2 = wait_for_confirmation(client2, txids2[0])

        # proposer_1 = get_block_proposer(client1, confirmed_round_1)
        # # proposer_2 = get_block_proposer(client2, confirmed_round_2)

        proposers_1.append(proposer_1)
        # proposers_2.append(proposer_2)
        confirmed_rounds_1.append(confirmed_round_1)
        # confirmed_rounds_2.append(confirmed_round_2)

        # proposers_1.append(proposer_1)
        # proposers_2.append(proposer_2)
        # confirmed_rounds_1.append(confirmed_round_1)
        # confirmed_rounds_2.append(confirmed_round_2)

        updated_value = print_global_state(client1, app_id)
        print("After Value: ", updated_value, "\n")

        if updated_value == "increment":
            print("decrement first")
            first_function = "Decrement"
            decrement_count += 1
            color = "red"  # Assign red color for Decrement
        elif updated_value == "decrement":
            print("increment first")
            first_function = "Increment"
            increment_count += 1
            color = "blue"

        # Append data to lists for scatter plot
        x_values.append(i)
        y_values.append(0) if first_function == "Increment" else y_values.append(1)
        colors.append(0) if color == "blue" else colors.append(1)
        print("before sleep")
        time.sleep(2)
        print("after sleep")

    # Calculate the total number of operations
    total_operations = increment_count + decrement_count

    # Calculate the percentage of increment and decrement operations
    percentage_increment = (increment_count / total_operations) * 100
    percentage_decrement = (decrement_count / total_operations) * 100

    # After the experiment, write the data to a CSV file
    with open("experiment_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Iteration",
                "Function",
                "Color",
                "Increment Count",
                "Increment Percentage",
                "Decrement Count",
                "Decrement Percentage",
                "Proposer 1",
                "confirmed_round_1",
                # "Proposer 2",
                # "confirmed_round_2"
            ]
        )
        for i in range(len(x_values)):
            writer.writerow(
                [
                    x_values[i],
                    y_values[i],
                    colors[i],
                    increment_count,
                    percentage_increment,
                    decrement_count,
                    percentage_decrement,
                    proposers_1[i],  # Use data from the list
                    confirmed_rounds_1[i],  # Use data from the list
                    # proposers_2[i],         # Use data from the list
                    # confirmed_rounds_2[i]   # Use data from the list
                ]
            )


def submit_and_wait_for_conf(client, atc):
    txids = submit_atc(atc, client)
    transaction_info, confirmed_round = wait_for_confirmation(client, txids[0])
    proposer = get_block_proposer(client, confirmed_round)
    return txids, transaction_info, confirmed_round, proposer


def get_block_proposer(client, confirmed_round: int):
    try:
        response = client.block_info(confirmed_round, response_format="msgpack")
        decoded_response = msgpack.unpackb(response, raw=True, strict_map_key=False)
        proposer = decoded_response[b"cert"][b"prop"][b"oprop"]
        proposer = algod.encoding.encode_address(proposer)
        return proposer
    except Exception as e:
        print(f"An error at block {confirmed_round} occurred: {e}")
        return None


def submit_atc(atc, client):
    return atc.submit(client)


def print_global_state(client, app_id):
    response = client.application_info(app_id)
    counter = None
    for item in response["params"]["global-state"]:
        key = base64.b64decode(item["key"]).decode("utf-8")
        if key == "counter":
            counter = base64.b64decode(item["value"]["bytes"]).decode("utf-8")
            return counter


def wait_for_confirmation(algod_client, txid, timeout=4):
    """
    Wait for the transaction to be confirmed.

    Args:
        algod_client (algosdk.algod.AlgodClient): Algorand client instance.
        txid (str): Transaction ID.
        timeout (int, optional): Maximum number of rounds to wait for confirmation. Defaults to 4.

    Returns:
        tuple: A tuple containing confirmed transaction information and the confirmed round.
    """
    last_round = algod_client.status().get("last-round")
    current_round = last_round + 1
    while current_round < last_round + timeout:
        try:
            # Check if the transaction is confirmed
            transaction_info = algod_client.pending_transaction_info(txid)
            confirmed_round = transaction_info.get("confirmed-round", 0)
            if confirmed_round > 0:
                return transaction_info, confirmed_round
        except Exception as e:
            print(f"Exception: {str(e)}")
            print(f"Waiting for confirmation... (current round: {current_round})")

        # Wait for the next round
        algod_client.status_after_block(current_round)
        current_round += 1

    raise Exception(f"Transaction not confirmed after {timeout} rounds")


def print_address(mn):
    pk_account_a = mnemonic.to_private_key(mn)
    address = account.address_from_private_key(pk_account_a)
    print("Creator Account Address :", address)


if __name__ == "__main__":
    generate_data()

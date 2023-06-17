import algosdk
import pyteal as pt
import algokit_utils

# from beaker import Application, Authorize, GlobalStateValue, sandbox
# from beaker.client import ApplicationClient
from algosdk import mnemonic, account, transaction, atomic_transaction_composer, abi
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.v2client import algod
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def main():
    token = ""
    headers = {"X-API-Key": os.getenv("TOKEN")}
    address = "https://testnet-algorand.api.purestake.io/ps2"
    client = algod.AlgodClient(token, address, headers)
    # demonstration purposes only, never use mnemonics in code
    mnemonic_1 = os.getenv("MNEMONIC")
    last_round = client.status()["last-round"]
    block_info = client.block_info(last_round)

    print("client: ", client.block_info())


if __name__ == "__main__":
    main()

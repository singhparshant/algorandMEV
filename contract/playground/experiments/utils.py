import os
from algosdk.v2client import algod
from algosdk.v2client import indexer

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def get_testnet_algod_client():
    algod_token = ""
    algod_headers = {"X-API-Key": os.getenv("TOKEN")}
    algod_server = "https://testnet-algorand.api.purestake.io/ps2"

    algod_client = algod.AlgodClient(algod_token, algod_server, algod_headers)
    return algod_client


def get_mainnet_algod_client():
    algod_token = ""
    algod_headers = {"X-API-Key": os.getenv("TOKEN")}
    algod_server = "https://mainnet-algorand.api.purestake.io/ps2"

    algod_client = algod.AlgodClient(algod_token, algod_server, algod_headers)
    return algod_client


def get_mainnet_indexer_client():
    indexer_token = ""
    indexer_headers = {"X-API-Key": os.getenv("TOKEN")}
    indexer_server = "https://mainnet-algorand.api.purestake.io/idx2"

    myindexer = indexer.IndexerClient(indexer_token, indexer_server, indexer_headers)
    return myindexer


def get_testnet_indexer_client():
    indexer_token = ""
    indexer_headers = {"X-API-Key": os.getenv("TOKEN")}
    indexer_server = "https://testnet-algorand.api.purestake.io/idx2"

    myindexer = indexer.IndexerClient(indexer_token, indexer_server, indexer_headers)
    return myindexer

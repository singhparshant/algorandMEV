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
    indexer_headers = {"X-API-Key": os.getenv("PURESTAKE_TOKEN")}
    indexer_server = "https://mainnet-algorand.api.purestake.io/idx2"

    myindexer = indexer.IndexerClient(indexer_token, indexer_server, indexer_headers)
    return myindexer


def get_testnet_indexer_client():
    indexer_token = ""
    indexer_headers = {"X-API-Key": os.getenv("PURESTAKE_TOKEN")}
    indexer_server = "https://testnet-algorand.api.purestake.io/idx2"

    myindexer = indexer.IndexerClient(indexer_token, indexer_server, indexer_headers)
    return myindexer


def get_testnet_TUM_algod_client():
    algod_server = "http://131.159.14.109:8081"
    algod_client = algod.AlgodClient(os.getenv("TOKEN_TUM_TESTNET"), algod_server)
    return algod_client


def get_mainnet_TUM_algod_client():
    algod_server = "http://131.159.14.109:8080"
    algod_client = algod.AlgodClient(
        algod_address=algod_server, algod_token=os.getenv("TOKEN_TUM_MAINNET")
    )
    return algod_client


def get_TUM_indexer_client():
    indexer_server = "https://mainnet-algorand.api.purestake.io/idx2"
    myindexer = indexer.IndexerClient(os.getenv("TOKEN_TUM_TESTNET"), indexer_server)
    return myindexer

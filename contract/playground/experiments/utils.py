import os
from algosdk.v2client import algod
from algosdk.v2client import indexer

from dotenv import load_dotenv

if load_dotenv(dotenv_path="../../../.env"):
    print("Environment variables loaded.")
else:
    print("Couldn't load environment variables.")


def get_testnet_algod_client():
    algod_token = ""
    algod_headers = {"X-API-Key": "jxSOmPn4DN3DpLNbylkiS2AMijXrb2Nl575cw3Fq"}
    print(algod_headers)
    algod_server = "https://testnet-algorand.api.purestake.io/ps2"

    algod_client = algod.AlgodClient(algod_token, algod_server, algod_headers)
    return algod_client


def get_mainnet_algod_client():
    algod_token = ""
    algod_headers = {"X-API-Key": "jxSOmPn4DN3DpLNbylkiS2AMijXrb2Nl575cw3Fq"}
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
    indexer_headers = {"X-API-Key": "jxSOmPn4DN3DpLNbylkiS2AMijXrb2Nl575cw3Fq"}
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
    indexer_headers = {"X-API-Key": "ODBHPZFSZLRGDZMJDMLR8B24GUKLFXAY"}
    indexer_server = (
        "https://mainnet-idx.algonode.network"  # "http://131.159.14.109:8981"
    )
    myindexer = indexer.IndexerClient(
        indexer_token="ODBHPZFSZLRGDZMJDMLR8B24GUKLFXAY",
        indexer_address=indexer_server,
        # indexer_headers=indexer_headers,
    )
    return myindexer

def get_testbed_algod_client():
    algod_server = "http://127.0.0.1:4100"
    algod_token = ""
    algod_headers = {
        "Authorization": "Bearer 97361fdc801fe9fd7f2ae87fa4ea5dc8b9b6ce7380c230eaf5494c4cb5d38d61"
    }
    algod_client = algod.AlgodClient(algod_token, algod_server, algod_headers)
    return algod_client

def get_test_non_part_1():
    algod_server = "http://192.168.30.5:4100"
    algod_token = ""
    algod_headers = {
        "Authorization": "Bearer 97361fdc801fe9fd7f2ae87fa4ea5dc8b9b6ce7380c230eaf5494c4cb5d38d61"
    }
    algod_client = algod.AlgodClient(algod_token, algod_server, algod_headers)
    return algod_client

def get_test_non_part_2():
    algod_server = "http://192.168.30.7:4100"
    algod_token = ""
    algod_headers = {
        "Authorization": "Bearer 97361fdc801fe9fd7f2ae87fa4ea5dc8b9b6ce7380c230eaf5494c4cb5d38d61"
    }
    algod_client = algod.AlgodClient(algod_token, algod_server, algod_headers)
    return algod_client

from http import client

from playground.experiments.utils import (
    get_testnet_indexer_client,
    get_testnet_algod_client,
)

from algosdk.atomic_transaction_composer import (
    ABIResult,
    AtomicTransactionComposer,
    TransactionSigner,
    TransactionWithSigner,
)


def dex_interaction():
    client = get_testnet_indexer_client()
    atc1 = AtomicTransactionComposer()


if __name__ == "__main__":
    dex_interaction()

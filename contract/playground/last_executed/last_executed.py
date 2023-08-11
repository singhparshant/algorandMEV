import algosdk
import pyteal as pt
import algokit_utils

# from beaker import Application, Authorize, GlobalStateValue, sandbox
# from beaker.client import ApplicationClient
from algosdk import mnemonic, account, transaction, atomic_transaction_composer, abi
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.v2client import algod

from beaker import (
    Application,
    Authorize,
    GlobalStateValue,
    sandbox,
    unconditional_create_approval,
)
import os
from playground.experiments.utils import get_testnet_algod_client
from playground.experiments.utils import get_testnet_TUM_algod_client
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from beaker.client import ApplicationClient


class LastExecutedState:
    counter = GlobalStateValue(
        stack_type=pt.TealType.bytes,
        default=pt.Bytes("None"),
        descr="A counter for showing how to use application state",
    )


last_executed = Application("LastExecutedApp", state=LastExecutedState()).apply(
    unconditional_create_approval, initialize_global_state=True
)


@last_executed.external(authorize=Authorize.only_creator())
def increment(*, output: pt.abi.String) -> pt.Expr:
    """increment the counter"""
    return pt.Seq(
        last_executed.state.counter.set(pt.Bytes("increment")),
        output.set(last_executed.state.counter),
    )


@last_executed.external(authorize=Authorize.only_creator())
def decrement(*, output: pt.abi.String) -> pt.Expr:
    """decrement the counter"""
    return pt.Seq(
        last_executed.state.counter.set(pt.Bytes("decrement")),
        output.set(last_executed.state.counter),
    )


def demo() -> None:
    # client = sandbox.get_algod_client()
    # demonstration purposes only, never use mnemonics in code
    mnemonic_1 = os.getenv("MNEMONIC")
    # client = algod.AlgodClient(token, address, headers)
    # client = get_testnet_TUM_algod_client()
    client = get_testnet_algod_client()

    # client = algokit_utils.get_algod_client(
    #     algokit_utils.AlgoClientConfig(address, token)
    # )

    # client = algokit_utils.get_algod_client(
    #     algokit_utils.AlgoClientConfig("http://localhost:4001", "a" * 64)
    # )
    # print_address(mnemonic_1)
    # print("client: ", client)
    # insert try catch here

    # accts = sandbox.get_accounts()
    # acct = accts.pop()
    private_key = mnemonic.to_private_key(mnemonic_1)
    print("Account address: ", account.address_from_private_key(private_key))
    # # Create an Application client containing both an algod client and my app
    app_client = ApplicationClient(
        client=client,
        app=last_executed,
        signer=AccountTransactionSigner(private_key),
    )

    print("app client: ", app_client)

    # Create the applicatiion on chain, set the app id for the app client
    app_id, app_addr, txid = app_client.create()
    print(f"Created App with id: {app_id} and address addr: {app_addr} in tx: {txid}")

    # noop_txn = transaction.ApplicationNoOpTxn(
    #     account.address_from_private_key(private_key), sp, app_id
    # )

    # ApplicationClient(client,  , AccountTransactionSigner(private_key))

    # app_client.call(increment)
    # Get suggested transaction parameters
    # params = client.suggested_params()

    # Define the method name and arguments
    # method_name = "increment"
    # method_args = []
    # txn = transaction.ApplicationCallTxn(
    #     account.address_from_private_key(private_key),
    #     params,
    #     212011117,
    #     transaction.OnComplete.NoOpOC,
    #     method_args,
    #     None,
    #     None,
    #     None,
    #     method_name,
    # )
    # signed_txn = txn.sign(private_key)

    # # Send the transaction
    # txid = client.send_transaction(signed_txn)
    # print("Transaction ID:", txid)

    # # Wait for transaction confirmation (define the wait_for_confirmation function if not already defined)
    # wait_for_confirmation(client, txid)
    # pending_txns = client.pending_transactions()

    # # Extract the transaction IDs from the list
    # print("pending_txns: ", pending_txns)
    # txn_ids = [txn.get("tx") for txn in pending_txns.get("transactions")]

    # Print the transaction IDs
    # print("Pending transaction IDs:", txn_ids)
    app_client.call(increment)
    app_client.call(decrement)
    print("app state: ", app_client.get_global_state())


# print(f"Currrent counter value: {result.return_value}")

# result = app_client.call(decrement)
# print(f"Currrent counter value: {result.return_value}")

# try:
#     # Try to call the increment method with a different signer, it should fail
#     # since we have the auth check
#     other_acct = accts.pop()
#     other_client = app_client.prepare(signer=other_acct.signer)
#     other_client.call(increment)
# except LogicError as e:
#     print(e)
#     print("App call failed as expected.")


def print_address(mn):
    pk_account_a = mnemonic.to_private_key(mn)
    address = account.address_from_private_key(pk_account_a)
    print("Creator Account Address :", address)


if __name__ == "__main__":
    demo()

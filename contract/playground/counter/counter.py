import pyteal as pt
from algokit_utils import LogicError
import algokit_utils

from beaker import (
    Application,
    Authorize,
    GlobalStateValue,
    sandbox,
)
from beaker.client import ApplicationClient
from algosdk import mnemonic
from algosdk import account
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.v2client import algod


class CounterState:
    counter = GlobalStateValue(
        stack_type=pt.TealType.uint64,
        descr="A counter for showing how to use application state",
    )


counter_app = Application("CounterApp", state=CounterState())


@counter_app.external(authorize=Authorize.only_creator())
def increment(*, output: pt.abi.Uint64) -> pt.Expr:
    """increment the counter"""
    return pt.Seq(
        counter_app.state.counter.set(counter_app.state.counter + pt.Int(1)),
        output.set(counter_app.state.counter),
    )


@counter_app.external(authorize=Authorize.only_creator())
def decrement(*, output: pt.abi.Uint64) -> pt.Expr:
    """decrement the counter"""
    return pt.Seq(
        counter_app.state.counter.set(counter_app.state.counter - pt.Int(1)),
        output.set(counter_app.state.counter),
    )


def demo() -> None:
    # client = sandbox.get_algod_client()
    token = ""
    headers = {"X-API-Key": "jxSOmPn4DN3DpLNbylkiS2AMijXrb2Nl575cw3Fq"}
    address = "https://testnet-algorand.api.purestake.io/ps2"
    # demonstration purposes only, never use mnemonics in code
    mnemonic_1 = "swear emerge betray stone path stamp vacant credit inmate wrist fury bronze sheriff era jacket wheel genius floor expose proof armor sorry blast abandon brave"

    client = algod.AlgodClient(token, address, headers)
    # client = algokit_utils.get_algod_client(
    #     algokit_utils.AlgoClientConfig(address, token)
    # )

    # client = algokit_utils.get_algod_client(
    #     algokit_utils.AlgoClientConfig("http://localhost:4001", "a" * 64)
    # )
    print_address(mnemonic_1)
    print("client: ", client)
    # insert try catch here

    # accts = sandbox.get_accounts()
    # acct = accts.pop()
    print("private_key: ", mnemonic.to_private_key(mnemonic_1))
    # Create an Application client containing both an algod client and my app
    app_client = ApplicationClient(
        client=client,
        app=counter_app,
        signer=AccountTransactionSigner(mnemonic.to_private_key(mnemonic_1)),
    )

    # app_client = ApplicationClient(
    #     client=client,
    #     app=counter_app,
    #     signer=acct.signer,
    # )

    # Create the applicatiion on chain, set the app id for the app client
    app_id, app_addr, txid = app_client.create()
    print(f"Created App with id: {app_id} and address addr: {app_addr} in tx: {txid}")

    app_client.call(increment)
    app_client.call(increment)
    app_client.call(increment)
    result = app_client.call(increment)
    print(f"Currrent counter value: {result.return_value}")

    result = app_client.call(decrement)
    print(f"Currrent counter value: {result.return_value}")

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

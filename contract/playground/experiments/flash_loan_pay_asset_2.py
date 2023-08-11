# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.
from pprint import pprint
from urllib.parse import quote_plus

from algosdk.future.transaction import AssetTransferTxn, PaymentTxn
from playground.experiments.utils import get_testnet_algod_client

from examples.v2.tutorial.common import get_account, get_assets
from examples.v2.utils import get_algod
from tinyman.v2.client import TinymanV2TestnetClient
from tinyman.v2.flash_swap import prepare_flash_swap_transactions
from tinyman.v2.formulas import calculate_flash_swap_asset_2_payment_amount
from algosdk import mnemonic, account, transaction
import os
from dotenv import load_dotenv

load_dotenv()

# account = get_account()
mnemonic_1 = os.getenv("MNEMONIC")
private_key = mnemonic.to_private_key(mnemonic_1)
account_address = account.address_from_private_key(private_key)

algod = get_testnet_algod_client()
client = TinymanV2TestnetClient(algod_client=algod, user_address=account_address)

# ASSET_A_ID, ASSET_B_ID = get_assets()["ids"]
ASSET_A_ID = 21582668  # TINYUSDC
ASSET_B_ID = 0  # ALGO

ASSET_A = client.fetch_asset(ASSET_A_ID)
ASSET_B = client.fetch_asset(ASSET_B_ID)
pool = client.fetch_pool(ASSET_A_ID, ASSET_B_ID)
# print("Pool Info: ", pool.info())

suggested_params = algod.suggested_params()
account_info = algod.account_info(account_address)

for asset in account_info["assets"]:
    if asset["asset-id"] == pool.asset_1.id:
        balance = asset["amount"]

asset_1_loan_amount = 1_000_000
asset_2_loan_amount = 0
asset_1_payment_amount = 1_000_000
asset_2_payment_amount = calculate_flash_swap_asset_2_payment_amount(
    asset_1_reserves=pool.asset_1_reserves,
    asset_2_reserves=pool.asset_2_reserves,
    total_fee_share=pool.total_fee_share,
    protocol_fee_ratio=pool.protocol_fee_ratio,
    asset_1_loan_amount=asset_1_loan_amount,
    asset_2_loan_amount=asset_2_loan_amount,
    asset_1_payment_amount=asset_1_payment_amount,
)

print("Asset 1 loan amount: ", asset_1_loan_amount)
print("Asset 2 loan amount: ", asset_2_loan_amount)
print("Asset 1 payment amount: ", asset_1_payment_amount)
print("Asset 2 payment amount: ", asset_2_payment_amount)

# Transfer amount is equal to sum of initial account balance and loan amount
# This transaction demonstrate that you can use the total amount
transfer_amount = balance + asset_1_loan_amount
print("Transfer amount: ", transfer_amount)
transactions = [
    # AssetTransferTxn(
    #     sender=account_address,
    #     sp=suggested_params,
    #     receiver=account_address,
    #     amt=transfer_amount,
    #     index=pool.asset_1.id,
    # )
]

if asset_1_payment_amount:
    transactions.append(
        AssetTransferTxn(
            sender=account_address,
            sp=suggested_params,
            receiver=pool.address,
            index=pool.asset_1.id,
            amt=asset_1_payment_amount,
        )
    )

if asset_2_payment_amount:
    if pool.asset_2.id:
        transactions.append(
            AssetTransferTxn(
                sender=account_address,
                sp=suggested_params,
                receiver=pool.address,
                index=pool.asset_2.id,
                amt=asset_2_payment_amount,
            )
        )
    else:
        transactions.append(
            PaymentTxn(
                sender=account_address,
                sp=suggested_params,
                receiver=pool.address,
                amt=asset_2_payment_amount,
            )
        )

txn_group = prepare_flash_swap_transactions(
    validator_app_id=pool.validator_app_id,
    asset_1_id=pool.asset_1.id,
    asset_2_id=pool.asset_2.id,
    asset_1_loan_amount=asset_1_loan_amount,
    asset_2_loan_amount=asset_2_loan_amount,
    transactions=transactions,
    suggested_params=suggested_params,
    sender=account_address,
)

# Sign
txn_group.sign_with_private_key(account_address, private_key)

# Submit transactions to the network and wait for confirmation
txn_info = client.submit(txn_group, wait=True)
print("Transaction Info")
print(txn_info)

print(
    f"Check the transaction group on Algoexplorer: https://testnet.algoexplorer.io/tx/group/{quote_plus(txn_group.id)}"
)

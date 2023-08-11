# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.
from playground.experiments.utils import get_mainnet_TUM_algod_client
from playground.experiments.utils import get_testnet_TUM_algod_client
from playground.experiments.utils import get_mainnet_algod_client
from tinyman.v2.client import TinymanV2TestnetClient, TinymanV2MainnetClient
from dotenv import load_dotenv
import os
from algosdk import mnemonic, account, transaction

load_dotenv()

mnemonic_1 = os.getenv("MNEMONIC")
private_key = mnemonic.to_private_key(mnemonic_1)
account_address = account.address_from_private_key(private_key)

# algod = get_mainnet_algod_client()
# algod = get_mainnet_algod_client()
# algod = get_mainnet_TUM_algod_client()
algod = get_testnet_TUM_algod_client()

client = TinymanV2TestnetClient(algod_client=algod, user_address=account_address)
# Fetch our two assets of interest
USDC = client.fetch_asset(10458941)
# USDC = client.fetch_asset(31566704)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(USDC, ALGO)
print(f"Pool Info: {pool.info()}")

# Get a quote for a swap of 1 ALGO to USDC with 1% slippage tolerance
quote = pool.fetch_fixed_input_swap_quote(amount_in=ALGO(1_000_000), slippage=0.01)
quote2 = pool.fetch_fixed_input_swap_quote(amount_in=ALGO(1_000_000), slippage=0.0)

print(quote)
print(f"USDC per ALGO: {quote.price}")
print(f"USDC per ALGO (worst case): {quote.price_with_slippage}")

print(quote2)
print(f"USDC per ALGO: {quote2.price}")
print(f"USDC per ALGO (worst case): {quote2.price_with_slippage}")

txn_group = pool.prepare_swap_transactions_from_quote(quote=quote)

sp = algod.suggested_params()
sp.note = "Adding a random value"
txn_group2 = pool.prepare_swap_transactions_from_quote(
    quote=quote2, suggested_params=sp
)

print("Pool Asset id: ", pool.pool_token_asset.id)

if not client.asset_is_opted_in(asset_id=10458941):
    # write code for Opt-in transaction to the asset if necessary
    opt_in_txn = transaction.AssetOptInTxn(
        sender=account_address,
        sp=algod.suggested_params(),
        index=10458941,
    )
    signed_optin_txn = opt_in_txn.sign(private_key)
    txid = algod.send_transaction(signed_optin_txn)

if not client.asset_is_opted_in(asset_id=pool.pool_token_asset.id):
    # Opt-in to the pool token
    opt_in_txn_group = pool.prepare_pool_token_asset_optin_transactions()
    # You can merge the transaction groups
    txn_group = txn_group + opt_in_txn_group

txn_group = txn_group2 + txn_group
# Sign
txn_group.sign_with_private_key(account_address, private_key)
# txn_group2.sign_with_private_key(account_address, private_key)

# Submit transactions to the network and wait for confirmation
# txn_info2 = client.submit(txn_group2, wait=False)
txn_info = client.submit(txn_group, wait=False)
print("Txn 1 submitted")


print("Transaction Info: ")
print(txn_info)

# print("Transaction Info2: ")
# print(txn_info2)

# print(
#     f"Check the transaction group on Algoexplorer: https://testnet.algoexplorer.io/tx/group/{quote_plus(txn_group.id)}"
# )
